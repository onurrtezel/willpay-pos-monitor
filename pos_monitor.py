"""
POS Monitor - Mevcut POS Sisteminden Veri Çekme
UI Automation ile başka bir POS programından veri okur ve WillPay'e gönderir
"""
import time
import sys
import requests
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import qrcode
from io import BytesIO
from PyQt6.QtGui import QPixmap

# Windows-only import
try:
    from pywinauto import Desktop, Application
    from pywinauto.findwindows import ElementNotFoundError
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("⚠️ pywinauto not available. This app works only on Windows.")

BACKEND_URL = "http://192.168.1.103:8000"


class QRPopup(QDialog):
    """QR Code popup dialog"""
    
    def __init__(self, qr_url, receipt_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Fiş - WillPay")
        self.setModal(True)
        self.resize(500, 600)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("✅ Fiş Hazır!")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # QR Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_label.setStyleSheet("background: white; padding: 20px; border-radius: 10px;")
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to QPixmap
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        
        qr_label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(qr_label)
        
        # Receipt info
        info_label = QLabel(f"Toplam: {receipt_data['total']}₺\nÜrün Sayısı: {receipt_data['item_count']}")
        info_label.setFont(QFont("Arial", 14))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # Close button
        close_btn = QPushButton("Kapat")
        close_btn.setFont(QFont("Arial", 12))
        close_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class POSMonitor(QMainWindow):
    """POS Monitor - Başka POS sisteminden veri çeken ana uygulama"""
    
    def __init__(self):
        super().__init__()
        self.pos_window = None
        self.is_monitoring = False
        self.last_receipt_data = None
        self.last_total_amount = None  # Son toplam tutar
        self.last_item_count = None    # Son ürün sayısı
        self.auto_start_enabled = True  # Otomatik başlatma aktif
        self.init_ui()
        
        # Auto-scan timer - HIZLANDIRILDI
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.scan_pos)
        
        # Otomatik başlatma timer
        self.startup_timer = QTimer()
        self.startup_timer.timeout.connect(self.auto_start)
        self.startup_timer.setSingleShot(True)
        self.startup_timer.start(2000)  # 2 saniye sonra otomatik başlat
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("WillPay POS Monitor - Otomatik Mod")
        self.setGeometry(100, 100, 800, 600)
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🔍 WillPay POS Monitor")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
        # Auto-start info
        auto_info = QLabel("🚀 Otomatik Mod: Program açılınca POS'a bağlanır ve izlemeyi başlatır")
        auto_info.setFont(QFont("Arial", 10))
        auto_info.setStyleSheet("""
            background: #d5f4e6;
            color: #27ae60;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)
        auto_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(auto_info)
        
        # Status
        self.status_label = QLabel("Durum: Otomatik başlatma bekliyor...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("""
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
        """)
        layout.addWidget(self.status_label)
        
        # POS Window Info
        info_layout = QVBoxLayout()
        
        label1 = QLabel("📝 İzlenecek POS Programı:")
        label1.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        info_layout.addWidget(label1)
        
        self.pos_name_input = QLabel("Pencere adını giriniz (örn: 'Restaurant POS', 'TouchBistro', vs.)")
        self.pos_name_input.setStyleSheet("""
            background: white;
            padding: 10px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
        """)
        info_layout.addWidget(self.pos_name_input)
        
        layout.addLayout(info_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("🔗 POS'a Bağlan")
        self.connect_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.connect_btn.setFixedHeight(50)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        self.connect_btn.clicked.connect(self.connect_to_pos)
        btn_layout.addWidget(self.connect_btn)
        
        self.start_btn = QPushButton("▶️ İzlemeyi Başlat")
        self.start_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.start_btn.setFixedHeight(50)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover:enabled {
                background: #229954;
            }
            QPushButton:disabled {
                background: #95a5a6;
            }
        """)
        self.start_btn.clicked.connect(self.toggle_monitoring)
        btn_layout.addWidget(self.start_btn)
        
        self.send_btn = QPushButton("📤 Manuel Gönder")
        self.send_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.send_btn.setFixedHeight(50)
        self.send_btn.setEnabled(False)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #e67e22;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover:enabled {
                background: #d35400;
            }
            QPushButton:disabled {
                background: #95a5a6;
            }
        """)
        self.send_btn.clicked.connect(self.manual_send)
        btn_layout.addWidget(self.send_btn)
        
        layout.addLayout(btn_layout)
        
        # Log area
        log_label = QLabel("📋 Log:")
        log_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(log_label)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            background: #2c3e50;
            color: #ecf0f1;
            font-family: 'Courier New';
            font-size: 11px;
            padding: 10px;
            border-radius: 8px;
        """)
        layout.addWidget(self.log_area)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def auto_start(self):
        """Otomatik başlatma - Program açılınca POS'a bağlan ve izlemeyi başlat"""
        if not self.auto_start_enabled:
            return
        
        self.log("🚀 Otomatik başlatma aktif...")
        self.log("💡 2 saniye sonra POS aranacak ve izleme başlayacak")
        
        # POS'a bağlan
        self.connect_to_pos()
        
        # Eğer bağlanıldıysa, izlemeyi başlat
        if self.pos_window is not None:
            # 1 saniye bekle
            QTimer.singleShot(1000, self.start_monitoring_auto)
        else:
            self.log("⚠️ POS bulunamadı - Manuel olarak bağlanmanız gerekiyor")
    
    def start_monitoring_auto(self):
        """Otomatik izlemeyi başlat"""
        if not self.is_monitoring and self.pos_window is not None:
            self.log("🔄 İzleme otomatik başlatılıyor...")
            self.toggle_monitoring()
        
    def log(self, message):
        """Add log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")
        
    def connect_to_pos(self):
        """Connect to POS window - Otomatik algılama"""
        if not WINDOWS_AVAILABLE:
            self.log("❌ Bu özellik sadece Windows'ta çalışır!")
            return
        
        self.log("🔍 POS penceresi aranıyor...")
        
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            
            self.log(f"📊 {len(windows)} pencere bulundu")
            
            # POS programı anahtar kelimeleri (otomatik algılama için)
            pos_keywords = [
                # Genel
                'POS', 'Point of Sale', 'Restaurant', 'Retail',
                'Kasa', 'Satış', 'Fiş', 'Kasiyerim',
                # Kendi POS'umuz
                'Granny', 'Waffle',  # ← pos_ui.py için
                # Uluslararası
                'Loyverse', 'Square', 'Toast', 'Clover',
                'TouchBistro', 'Lightspeed', 'Revel',
                'Micros', 'NCR', 'Aloha', 'Maitre',
                'Odoo',  # ← Odoo için
                # Türk Programlar
                'Logo', 'Nebim', 'Mikro', 'Param',
                # Test için
                'Sale', 'Cash Register', 'Checkout'
            ]
            
            # Tüm pencereleri tara ve POS olanı bul
            pos_windows = []
            other_windows = []
            
            for i, window in enumerate(windows):
                try:
                    title = window.window_text()
                    if not title or len(title) < 3:
                        continue
                    
                    # Sistem pencerelerini atla
                    skip_keywords = ['Program Manager', 'MSCTFIME UI', 'Default IME']
                    if any(skip in title for skip in skip_keywords):
                        continue
                    
                    # POS programı mı kontrol et
                    is_pos = any(keyword.lower() in title.lower() for keyword in pos_keywords)
                    
                    if is_pos:
                        self.log(f"  ✅ POS bulundu: {title}")
                        pos_windows.append((title, window))
                    else:
                        self.log(f"  ℹ️  Diğer: {title}")
                        other_windows.append((title, window))
                        
                except:
                    pass
            
            # POS penceresi bulundu mu?
            if pos_windows:
                # İlk POS penceresini seç
                selected_title, selected_window = pos_windows[0]
                self.pos_window = selected_window
                
                self.pos_name_input.setText(f"✅ Otomatik Bulundu: {selected_title}")
                self.status_label.setText(f"Durum: Bağlı - {selected_title}")
                self.status_label.setStyleSheet("""
                    background: #d5f4e6;
                    color: #27ae60;
                    padding: 15px;
                    border-radius: 8px;
                    font-weight: bold;
                """)
                self.start_btn.setEnabled(True)
                self.send_btn.setEnabled(True)
                
                self.log(f"✅ POS penceresine otomatik bağlanıldı: {selected_title}")
                
                if len(pos_windows) > 1:
                    self.log(f"ℹ️  Not: {len(pos_windows)} POS penceresi bulundu, ilki seçildi")
                    
            elif other_windows:
                # POS bulunamadı ama başka pencereler var
                self.log("⚠️ POS penceresi otomatik algılanamadı!")
                self.log(f"ℹ️  {len(other_windows)} başka pencere bulundu:")
                
                for i, (title, _) in enumerate(other_windows[:5], 1):
                    self.log(f"     {i}. {title}")
                
                # İlk pencereyi manuel seçim için öner
                if other_windows:
                    self.log(f"💡 İlk pencereye bağlanılıyor: {other_windows[0][0]}")
                    self.pos_window = other_windows[0][1]
                    self.pos_name_input.setText(f"⚠️ Manuel: {other_windows[0][0]}")
                    self.status_label.setText(f"Durum: Manuel - {other_windows[0][0]}")
                    self.status_label.setStyleSheet("""
                        background: #fff3cd;
                        color: #856404;
                        padding: 15px;
                        border-radius: 8px;
                        font-weight: bold;
                    """)
                    self.start_btn.setEnabled(True)
                    self.send_btn.setEnabled(True)
            else:
                self.log("❌ Hiç uygun pencere bulunamadı!")
                
        except Exception as e:
            self.log(f"❌ Hata: {str(e)}")
            
    def toggle_monitoring(self):
        """Start/stop monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.setText("⏸️ İzlemeyi Durdur")
            self.scan_timer.start(500)  # SÜREKLI: Her 0.5 saniyede (500ms)
            self.log("▶️ İzleme başlatıldı (sürekli tarama - 0.5s aralık)")
            self.log("💡 Değişiklik algılandığında otomatik gönderilecek")
        else:
            self.is_monitoring = False
            self.start_btn.setText("▶️ İzlemeyi Başlat")
            self.scan_timer.stop()
            self.last_total_amount = None
            self.last_item_count = None
            self.log("⏸️ İzleme durduruldu")
            
    def scan_pos(self):
        """Scan POS window for receipt data - DEĞİŞİKLİK ALGILAMALI"""
        if not self.pos_window:
            return
        
        try:
            # Tüm text elementlerini bul
            texts = []
            numbers = []  # Sayısal değerler (fiyatlar)
            
            try:
                controls = self.pos_window.descendants()
                for control in controls:
                    try:
                        if control.control_type() == "Text":
                            text = control.window_text()
                            if text and len(text) > 0:
                                texts.append(text)
                                
                                # Sayı içeren metinleri ayır (fiyat, tutar)
                                if any(char.isdigit() for char in text):
                                    numbers.append(text)
                    except:
                        pass
            except:
                pass
            
            if not texts:
                return
            
            # Toplam tutar ve ürün sayısını bulmaya çalış
            current_total = self.extract_total(texts, numbers)
            current_item_count = len([t for t in texts if any(kw in t.lower() for kw in ['₺', 'tl', 'lira', '$'])])
            
            # DEĞİŞİKLİK ALGILAMA
            if current_total is not None:
                # İlk okuma
                if self.last_total_amount is None:
                    self.last_total_amount = current_total
                    self.last_item_count = current_item_count
                    self.log(f"📊 İlk okuma: {current_total}₺ - {current_item_count} öğe")
                    
                # Değişiklik var mı?
                elif current_total != self.last_total_amount:
                    self.log(f"🔔 DEĞİŞİKLİK ALGILANDI!")
                    self.log(f"   Önceki: {self.last_total_amount}₺ → Yeni: {current_total}₺")
                    
                    # Tutar arttıysa (yeni ürün eklendi)
                    if current_total > self.last_total_amount:
                        self.log(f"   ➕ Ürün eklendi")
                        
                    # Tutar azaldıysa (ürün çıkarıldı)
                    elif current_total < self.last_total_amount:
                        self.log(f"   ➖ Ürün çıkarıldı")
                    
                    # Tutar 0'a döndüyse (ödeme tamamlandı - OTOMATIK GÖNDER)
                    if self.last_total_amount > 0 and current_total == 0:
                        self.log(f"💳 ÖDEME TAMAMLANDI! Otomatik gönderiliyor...")
                        self.auto_send_receipt(self.last_total_amount)
                    
                    # Güncel değerleri kaydet
                    self.last_total_amount = current_total
                    self.last_item_count = current_item_count
                else:
                    # Değişiklik yok - sessiz tarama
                    pass
            
        except Exception as e:
            self.log(f"⚠️ Tarama hatası: {str(e)}")
    
    def extract_total(self, texts, numbers):
        """Metinlerden toplam tutarı çıkar"""
        try:
            # "Toplam", "Total", "TOTAL", "Tutar" gibi anahtar kelimeler ara
            total_keywords = ['toplam', 'total', 'tutar', 'ödenecek', 'toplam tutar']
            
            for i, text in enumerate(texts):
                text_lower = text.lower()
                
                # Anahtar kelime var mı?
                if any(kw in text_lower for kw in total_keywords):
                    # Hemen yanındaki sayıyı bul
                    for j in range(max(0, i-2), min(len(texts), i+3)):
                        try:
                            # Sayıyı çıkar
                            num_text = texts[j].replace('₺', '').replace('TL', '').replace(',', '.').strip()
                            num = float(''.join(c for c in num_text if c.isdigit() or c == '.'))
                            if num > 0:
                                return num
                        except:
                            pass
            
            # Bulunamadıysa, en büyük sayıyı al (muhtemelen toplam)
            max_num = 0
            for num_text in numbers:
                try:
                    cleaned = num_text.replace('₺', '').replace('TL', '').replace(',', '.').strip()
                    num = float(''.join(c for c in cleaned if c.isdigit() or c == '.'))
                    if num > max_num:
                        max_num = num
                except:
                    pass
            
            return max_num if max_num > 0 else None
            
        except:
            return None
    
    def auto_send_receipt(self, total_amount):
        """Otomatik fiş gönder - Ödeme tamamlandığında"""
        self.log(f"📤 Otomatik gönderim: {total_amount}₺")
        
        # Demo receipt data
        receipt_data = {
            "user_id": 1,
            "store_name": "Granny's Waffle",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_amount": total_amount,
            "category": "food",
            "is_favorite": False,
            "notes": "POS Monitor - Otomatik Gönderim",
            "image_url": None,
            "items": [
                {"name": "POS Ürün", "price": total_amount, "quantity": 1, "category": "general"}
            ]
        }
        
        self.send_to_backend(receipt_data)
            
    def manual_send(self):
        """Manually send receipt to backend"""
        self.log("📤 Manuel gönderim başlatıldı...")
        
        # Demo data - gerçekte POS'tan okunmalı
        receipt_data = {
            "user_id": 1,
            "store_name": "Granny's Waffle",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_amount": 90.0,
            "category": "food",
            "is_favorite": False,
            "notes": "POS Monitor - Manuel Gönderim",
            "image_url": None,
            "items": [
                {"name": "Çikolatalı Waffle", "price": 35.0, "quantity": 1, "category": "waffle"},
                {"name": "Türk Kahvesi", "price": 15.0, "quantity": 1, "category": "kahve"}
            ]
        }
        
        self.send_to_backend(receipt_data)
        
    def send_to_backend(self, receipt_data):
        """Send receipt to WillPay backend"""
        try:
            self.log(f"📤 Backend'e gönderiliyor: {BACKEND_URL}/receipts")
            
            response = requests.post(
                f"{BACKEND_URL}/receipts",
                json=receipt_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                
                # Handle array response
                if isinstance(result, list):
                    receipt_id = result[0]
                    total = float(result[4])
                else:
                    receipt_id = result.get('id')
                    total = result.get('totalAmount', receipt_data['total_amount'])
                
                self.log(f"✅ Fiş oluşturuldu: ID={receipt_id}")
                
                # QR URL oluştur
                import json
                from urllib.parse import quote
                
                store_name = receipt_data['store_name']
                items_json = json.dumps(receipt_data['items'])
                
                store_encoded = quote(store_name)
                items_encoded = quote(items_json)
                
                qr_url = f"{BACKEND_URL}/receipt/new?amount={total}&store={store_encoded}&items={items_encoded}"
                
                # QR popup göster
                popup_data = {
                    'total': total,
                    'item_count': len(receipt_data['items'])
                }
                
                dialog = QRPopup(qr_url, popup_data, self)
                dialog.exec()
                
                self.log("✅ QR kod gösterildi!")
                
            else:
                self.log(f"❌ Backend hatası: {response.status_code}")
                self.log(f"   {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            self.log(f"❌ Backend'e bağlanılamadı: {BACKEND_URL}")
        except Exception as e:
            self.log(f"❌ Hata: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = POSMonitor()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


