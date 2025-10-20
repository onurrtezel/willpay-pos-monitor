"""
WillPay POS UI - Granny's Waffle
Windows POS interface with UI Automation support
"""
import sys
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame, QGridLayout, QDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
import qrcode
from io import BytesIO


# Sample product database
PRODUCTS = {
    "Waffle": [
        {"name": "Çikolatalı Waffle", "price": 35, "emoji": "🍫"},
        {"name": "Muzlu Waffle", "price": 30, "emoji": "🍌"},
        {"name": "Çilekli Waffle", "price": 32, "emoji": "🍓"},
        {"name": "Karamelli Waffle", "price": 33, "emoji": "🍯"},
    ],
    "Smoothie": [
        {"name": "Karışık Smoothie", "price": 25, "emoji": "🥤"},
        {"name": "Çilekli Smoothie", "price": 22, "emoji": "🍓"},
        {"name": "Mango Smoothie", "price": 28, "emoji": "🥭"},
        {"name": "Yaban Mersini Smoothie", "price": 26, "emoji": "🫐"},
    ],
    "Kahve": [
        {"name": "Türk Kahvesi", "price": 15, "emoji": "☕"},
        {"name": "Espresso", "price": 18, "emoji": "☕"},
        {"name": "Cappuccino", "price": 20, "emoji": "☕"},
        {"name": "Latte", "price": 22, "emoji": "☕"},
    ],
}

# WillPay Backend Configuration
BACKEND_URL = "http://localhost:8000"  # Backend'e istek için
QR_FRONTEND_URL = "http://192.168.1.103:3000"  # QR kod için (Frontend - mevcut fişi göster)


class QRPopup(QDialog):
    """QR Code popup dialog - Modern design"""
    
    def __init__(self, qr_url, receipt_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Fiş - Granny's Waffle")
        self.setModal(True)
        self.resize(600, 800)
        
        # Modern background
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title - Big and bold
        title = QLabel("✅ Ödeme Başarılı!")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            padding: 20px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
        """)
        layout.addWidget(title)
        
        # Instruction - Bigger text
        instruction = QLabel("📱 Fişinizi almak için QR kodu okutun")
        instruction.setFont(QFont("Segoe UI", 16))
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet("""
            color: rgba(255, 255, 255, 0.95);
            padding: 10px;
            font-weight: 500;
        """)
        layout.addWidget(instruction)
        
        # QR Code container - Modern white card
        qr_container = QFrame()
        qr_container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 20px;
                padding: 30px;
            }
        """)
        qr_container_layout = QVBoxLayout()
        
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
        
        qr_label.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio))
        qr_container_layout.addWidget(qr_label)
        
        qr_container.setLayout(qr_container_layout)
        layout.addWidget(qr_container)
        
        # Receipt details - Modern card
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)
        
        receipt_title = QLabel("📄 Fiş Özeti")
        receipt_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        receipt_title.setStyleSheet("color: #2c3e50; padding-bottom: 10px;")
        details_layout.addWidget(receipt_title)
        
        for item in receipt_data['items']:
            item_text = f"• {item['name']} ✕ {item['quantity']} = {item['price'] * item['quantity']}₺"
            item_label = QLabel(item_text)
            item_label.setFont(QFont("Segoe UI", 13))
            item_label.setStyleSheet("color: #495057; padding: 5px;")
            details_layout.addWidget(item_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: #dee2e6; margin: 10px 0;")
        details_layout.addWidget(separator)
        
        total_label = QLabel(f"Toplam: {receipt_data['totalAmount']}₺")
        total_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        total_label.setStyleSheet("""
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #56ab2f, stop:1 #a8e063);
            padding: 15px;
            border-radius: 10px;
        """)
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        details_layout.addWidget(total_label)
        
        details_frame.setLayout(details_layout)
        layout.addWidget(details_frame)
        
        # Close button - Modern large button
        close_btn = QPushButton("✓ Tamam")
        close_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        close_btn.setFixedHeight(60)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.25);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.5);
                padding: 15px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.35);
                border: 2px solid rgba(255, 255, 255, 0.7);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class POSMainWindow(QMainWindow):
    """Main POS window with UI Automation support"""
    
    def __init__(self):
        super().__init__()
        self.cart = []  # List of cart items
        self.is_processing_payment = False  # Prevent double payment
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Granny's Waffle - POS System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Modern stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # LEFT PANEL - Products
        left_panel = self.create_products_panel()
        main_layout.addWidget(left_panel, 2)
        
        # RIGHT PANEL - Cart
        right_panel = self.create_cart_panel()
        main_layout.addWidget(right_panel, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def create_products_panel(self):
        """Create left panel with product categories and items"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-right: 2px solid #dee2e6;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Title - Modern header
        title = QLabel("🧇 Granny's Waffle")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: #2c3e50;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 12px;
            color: white;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Menü Seçimi")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #6c757d; padding: 5px 10px;")
        layout.addWidget(subtitle)
        
        # Scroll area for products
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(20)
        
        # Add categories
        for category, products in PRODUCTS.items():
            category_widget = self.create_category_section(category, products)
            scroll_layout.addWidget(category_widget)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        panel.setLayout(layout)
        
        return panel
    
    def create_category_section(self, category, products):
        """Create a category section with product buttons"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e9ecef;
            }
            QFrame:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        # Category title - Modern
        title = QLabel(f"📂 {category}")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("""
            color: #495057;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        """)
        layout.addWidget(title)
        
        # Products grid
        grid = QGridLayout()
        grid.setSpacing(10)
        
        for i, product in enumerate(products):
            row = i // 2
            col = i % 2
            btn = self.create_product_button(product, category)
            grid.addWidget(btn, row, col)
        
        layout.addLayout(grid)
        frame.setLayout(layout)
        
        return frame
    
    def create_product_button(self, product, category):
        """Create a product button - Modern design"""
        btn = QPushButton()
        btn.setFixedSize(320, 110)
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 18px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #764ba2, stop:1 #667eea);
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a4a8a, stop:1 #4a5fc0);
            }
        """)
        
        # Emoji ve isim ayrı satırlarda, fiyat vurgulu
        text = f"{product['emoji']}  {product['name']}\n💰 {product['price']}₺"
        btn.setText(text)
        btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        btn.clicked.connect(lambda: self.add_to_cart(product, category))
        
        return btn
    
    def add_to_cart(self, product, category):
        """Add product to cart"""
        # Check if product already in cart
        for item in self.cart:
            if item['name'] == product['name']:
                item['quantity'] += 1
                self.update_cart_display()
                return
        
        # Add new item
        self.cart.append({
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'category': category
        })
        self.update_cart_display()
    
    def create_cart_panel(self):
        """Create right panel with cart and checkout - Modern design"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title - Modern header
        title_container = QFrame()
        title_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        title_layout = QVBoxLayout()
        
        title = QLabel("🛒 Sepetim")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        title_container.setLayout(title_layout)
        layout.addWidget(title_container)
        
        # Cart items scroll area (Normal mod)
        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.cart_items_widget = QWidget()
        self.cart_items_layout = QVBoxLayout()
        self.cart_items_layout.setSpacing(10)
        self.cart_items_widget.setLayout(self.cart_items_layout)
        self.cart_scroll.setWidget(self.cart_items_widget)
        
        layout.addWidget(self.cart_scroll, 1)  # Stretch factor - QR ile aynı alan
        
        # QR Display area (hidden by default) - Sepet yerine gösterilecek
        self.qr_display_container = QFrame()
        self.qr_display_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        qr_display_layout = QVBoxLayout()
        qr_display_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_display_layout.setContentsMargins(0, 0, 0, 0)
        qr_display_layout.setSpacing(10)
        
        # QR mesajı
        self.qr_message = QLabel("📱 QR Kodu Taratın")
        self.qr_message.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.qr_message.setStyleSheet("""
            color: white;
            background: rgba(255, 255, 255, 0.15);
            padding: 12px;
            border-radius: 10px;
        """)
        self.qr_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # QR için beyaz arka plan container
        qr_white_bg = QFrame()
        qr_white_bg.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        qr_bg_layout = QVBoxLayout()
        qr_bg_layout.setContentsMargins(15, 15, 15, 15)
        qr_bg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_display.setScaledContents(False)  # Aspect ratio koru
        
        qr_bg_layout.addWidget(self.qr_display)
        qr_white_bg.setLayout(qr_bg_layout)
        
        qr_display_layout.addWidget(self.qr_message)
        qr_display_layout.addWidget(qr_white_bg)
        qr_display_layout.addStretch()
        
        self.qr_display_container.setLayout(qr_display_layout)
        self.qr_display_container.hide()  # Başlangıçta gizli
        layout.addWidget(self.qr_display_container, 1)  # Stretch factor ekle
        
        # Total amount (UI Automation accessible) - Modern
        self.total_label = QLabel("Toplam: 0₺")
        self.total_label.setObjectName("TotalLabel")  # AutomationId
        self.total_label.setAccessibleName("TotalLabel")
        self.total_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        self.total_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f093fb, stop:1 #f5576c);
                color: white;
                padding: 25px;
                border-radius: 15px;
                border: 3px solid rgba(255, 255, 255, 0.3);
            }
        """)
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_label)
        
        # Pay button (UI Automation accessible) - Modern giant button
        self.pay_button = QPushButton("💳 Ödeme Tamamla")
        self.pay_button.setObjectName("PayButton")  # AutomationId
        self.pay_button.setAccessibleName("PayButton")
        self.pay_button.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.pay_button.setFixedHeight(85)
        self.pay_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #56ab2f, stop:1 #a8e063);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a8e063, stop:1 #56ab2f);
                padding: 2px;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a9428, stop:1 #8bc653);
            }
            QPushButton:disabled {
                background: #95a5a6;
                color: #ecf0f1;
            }
        """)
        self.pay_button.clicked.connect(self.complete_payment)
        self.pay_button.setEnabled(False)
        layout.addWidget(self.pay_button)
        
        # Clear cart button - Modern subtle design
        clear_button = QPushButton("🗑️ Sepeti Temizle")
        clear_button.setFont(QFont("Segoe UI", 14))
        clear_button.setFixedHeight(55)
        clear_button.setStyleSheet("""
            QPushButton {
                background: rgba(231, 76, 60, 0.9);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(192, 57, 43, 1);
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(169, 50, 38, 1);
            }
        """)
        clear_button.clicked.connect(self.clear_cart)
        layout.addWidget(clear_button)
        
        panel.setLayout(layout)
        
        return panel
    
    def update_cart_display(self):
        """Update cart display with current items"""
        # Clear existing items
        while self.cart_items_layout.count():
            child = self.cart_items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Add cart items
        for i, item in enumerate(self.cart):
            item_widget = self.create_cart_item_widget(item, i)
            self.cart_items_layout.addWidget(item_widget)
        
        self.cart_items_layout.addStretch()
        
        # Update total
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        self.total_label.setText(f"Toplam: {total}₺")
        
        # Enable/disable pay button
        self.pay_button.setEnabled(len(self.cart) > 0)
    
    def create_cart_item_widget(self, item, index):
        """Create widget for a cart item - Modern card design"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Item name (UI Automation accessible) - Bigger and bolder
        name_label = QLabel(item['name'])
        name_label.setObjectName(f"receipt_item_{index}_name")
        name_label.setAccessibleName(f"receipt_item_{index}_name")
        name_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white; padding: 2px;")
        layout.addWidget(name_label)
        
        # Price and quantity (UI Automation accessible) - Modern info row
        info_layout = QHBoxLayout()
        
        price_label = QLabel(f"{item['price']}₺")
        price_label.setObjectName(f"receipt_item_{index}_price")
        price_label.setAccessibleName(f"receipt_item_{index}_price")
        price_label.setFont(QFont("Segoe UI", 13))
        price_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        quantity_label = QLabel(f"✕ {item['quantity']}")
        quantity_label.setObjectName(f"receipt_item_{index}_quantity")
        quantity_label.setAccessibleName(f"receipt_item_{index}_quantity")
        quantity_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        quantity_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        
        subtotal_label = QLabel(f"{item['price'] * item['quantity']}₺")
        subtotal_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        subtotal_label.setStyleSheet("""
            color: #a8e063;
            background: rgba(168, 224, 99, 0.2);
            padding: 4px 12px;
            border-radius: 6px;
        """)
        
        info_layout.addWidget(price_label)
        info_layout.addWidget(quantity_label)
        info_layout.addStretch()
        info_layout.addWidget(subtotal_label)
        
        layout.addLayout(info_layout)
        
        # Remove button - Modern circular button
        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(35, 35)
        remove_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        remove_btn.setStyleSheet("""
            QPushButton {
                background: rgba(231, 76, 60, 0.8);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 17px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(231, 76, 60, 1);
                border: 2px solid rgba(255, 255, 255, 0.5);
                transform: scale(1.1);
            }
            QPushButton:pressed {
                background: rgba(192, 57, 43, 1);
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_from_cart(index))
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)
        
        frame.setLayout(layout)
        
        return frame
    
    def remove_from_cart(self, index):
        """Remove item from cart"""
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            self.update_cart_display()
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.clear()
        self.update_cart_display()
        
        # QR gösteriliyorsa gizle, sepeti göster
        self.cart_scroll.show()
        self.qr_display_container.hide()
        self.pay_button.setText("💳 Ödeme Tamamla")
    
    def show_qr_in_panel(self, qr_url, total_amount):
        """Sepet panelinde QR göster"""
        import qrcode
        from io import BytesIO
        
        # QR kod oluştur
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # QPixmap'e çevir
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read())
        
        # QR'ı göster - Kompakt boyut
        scaled_pixmap = pixmap.scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.qr_display.setPixmap(scaled_pixmap)
        self.qr_display.setFixedSize(220, 220)  # Kare şekil - kompakt
        
        # Sepeti gizle, QR'ı göster
        self.cart_scroll.hide()
        self.qr_display_container.show()
        
        # Sepeti temizle
        self.cart.clear()
        self.total_label.setText(f"✅ QR Hazır: {total_amount}₺")
    
    def complete_payment(self):
        """Complete payment and show QR in panel"""
        # Eğer buton "Yeni Sipariş" modundaysa, temizle ve normale dön
        if self.pay_button.text() == "🔄 Yeni Sipariş":
            self.clear_cart()
            return
        
        if not self.cart:
            return
        
        # 🔒 CRITICAL: Prevent double payment
        if self.is_processing_payment:
            print("⚠️ Payment already in progress, ignoring...")
            return
        
        self.is_processing_payment = True
        print("🔒 Payment locked")
        
        # Disable pay button to prevent double submission
        self.pay_button.setEnabled(False)
        self.pay_button.setText("İşleniyor...")
        
        from datetime import datetime
        
        # Prepare receipt data for WillPay backend
        total_amount = sum(item['price'] * item['quantity'] for item in self.cart)
        
        receipt_data = {
            "user_id": 1,  # WillPay backend requires user_id (integer)
            "store_name": "Granny's Waffle",
            "date": datetime.now().strftime("%Y-%m-%d"),  # WillPay backend requires date
            "total_amount": total_amount,
            "category": "food",  # Category for the receipt
            "is_favorite": False,
            "notes": "POS Payment - Granny's Waffle",
            "image_url": None,
            "items": [
                {
                    "name": item['name'],
                    "price": float(item['price']),
                    "quantity": item['quantity'],
                    "category": item['category'].lower()
                }
                for item in self.cart
            ]
        }
        
        # QR oluştur - Backend'e KAYDETMEDEN!
        # Landing page parametreleri alıp kendisi backend'e kaydedecek
        from urllib.parse import quote
        import json
        
        try:
            print(f"📝 QR kod hazırlanıyor (backend'e kaydetmeden)...")
            
            store_name = "Granny's Waffle"
            
            # Items JSON oluştur
            items_json = json.dumps([
                {
                    "name": item['name'],
                    "price": float(item['price']),
                    "quantity": item['quantity'],
                    "category": item['category'].lower()
                }
                for item in self.cart
            ])
            
            # URL encode
            store_encoded = quote(store_name)
            items_encoded = quote(items_json)
            
            # QR URL formatı: /receipt/new SADECE parametreler (receiptId YOK!)
            # Landing page bu parametrelerle YENİ fiş oluşturacak
            qr_url = f"http://172.20.10.4:8000/receipt/new?amount={total_amount}&store={store_encoded}&items={items_encoded}"
            
            print(f"🎯 QR URL: {qr_url[:100]}...")
            print(f"🎯 Store: {store_name}")
            print(f"🎯 Amount: {total_amount}₺")
            print(f"🎯 Items: {len(self.cart)} adet")
            print(f"💡 Landing page QR parametrelerinden fiş oluşturacak")
            
            # QR'ı sepet panelinde göster (popup yok!)
            self.show_qr_in_panel(qr_url, total_amount)
            
            print("✅ QR sepet panelinde gösteriliyor!")
            
            # Re-enable pay button (yeni sipariş için)
            self.pay_button.setText("🔄 Yeni Sipariş")
            self.pay_button.setEnabled(True)
            self.is_processing_payment = False
            print("🔓 Payment unlocked")
            
        except Exception as e:
            print(f"❌ Backend bağlantı hatası!")
            print(f"💡 Backend çalışmıyor: {BACKEND_URL}")
            print(f"   Fiş kaydedilemedi ama devam edebilirsiniz")
            
            # Kullanıcıya bildir
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Backend Hatası",
                f"Backend'e bağlanılamadı!\n\n"
                f"URL: {BACKEND_URL}\n\n"
                f"Fiş kaydedilemedi.\n"
                f"Backend'i kontrol edin.",
                QMessageBox.StandardButton.Ok
            )
            
            # Re-enable pay button on error
            self.pay_button.setEnabled(True)
            self.pay_button.setText("💳 Ödeme Tamamla")
            
            # 🔓 Unlock payment on error
            self.is_processing_payment = False
            print("🔓 Payment unlocked (connection error)")
            
        except requests.exceptions.Timeout:
            print(f"❌ Backend timeout! 3 saniyede yanıt vermedi")
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Timeout Hatası",
                "Backend çok yavaş yanıt veriyor!\n\n"
                "3 saniyeden uzun sürdü.\n"
                "Backend'i kontrol edin.",
                QMessageBox.StandardButton.Ok
            )
            
            self.pay_button.setEnabled(True)
            self.pay_button.setText("💳 Ödeme Tamamla")
            self.is_processing_payment = False
            print("🔓 Payment unlocked (timeout)")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Re-enable pay button on error
            self.pay_button.setEnabled(True)
            self.pay_button.setText("💳 Ödeme Tamamla")
            
            # 🔓 Unlock payment on error
            self.is_processing_payment = False
            print("🔓 Payment unlocked (exception)")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = POSMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

