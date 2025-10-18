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
BACKEND_URL = "http://192.168.1.103:8000"  # Mevcut WillPay Backend
# BACKEND_URL = "http://localhost:8000"  # Localhost için


class QRPopup(QDialog):
    """QR Code popup dialog"""
    
    def __init__(self, qr_url, receipt_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QR Fiş - Granny's Waffle")
        self.setModal(True)
        self.resize(500, 700)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("✅ Ödeme Tamamlandı!")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Instruction
        instruction = QLabel("Fişinizi almak için QR kodu okutun")
        instruction.setFont(QFont("Arial", 12))
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet("color: #666;")
        layout.addWidget(instruction)
        
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
        
        # Receipt details
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background: #f5f5f5;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        details_layout = QVBoxLayout()
        
        receipt_title = QLabel("📄 Fiş Detayları")
        receipt_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        details_layout.addWidget(receipt_title)
        
        for item in receipt_data['items']:
            item_text = f"{item['name']} x{item['quantity']} - {item['price'] * item['quantity']}₺"
            item_label = QLabel(item_text)
            item_label.setFont(QFont("Arial", 11))
            details_layout.addWidget(item_label)
        
        total_label = QLabel(f"\nToplam: {receipt_data['totalAmount']}₺")
        total_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        total_label.setStyleSheet("color: #2c3e50;")
        details_layout.addWidget(total_label)
        
        details_frame.setLayout(details_layout)
        layout.addWidget(details_frame)
        
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
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
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
        self.setGeometry(100, 100, 1200, 800)
        
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
        panel.setStyleSheet("background: #ecf0f1;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🧇 Granny's Waffle - Ürünler")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)
        
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
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Category title
        title = QLabel(f"📂 {category}")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #34495e;")
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
        """Create a product button"""
        btn = QPushButton()
        btn.setFixedSize(280, 100)
        btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                text-align: left;
                padding: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:pressed {
                background: #21618c;
            }
        """)
        
        text = f"{product['emoji']} {product['name']}\n{product['price']}₺"
        btn.setText(text)
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
        """Create right panel with cart and checkout"""
        panel = QFrame()
        panel.setStyleSheet("background: #2c3e50;")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🛒 Sepet")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; padding: 10px;")
        layout.addWidget(title)
        
        # Cart items scroll area
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
        
        layout.addWidget(self.cart_scroll)
        
        # Total amount (UI Automation accessible)
        self.total_label = QLabel("Toplam: 0₺")
        self.total_label.setObjectName("TotalLabel")  # AutomationId
        self.total_label.setAccessibleName("TotalLabel")
        self.total_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.total_label.setStyleSheet("""
            background: #34495e;
            color: white;
            padding: 20px;
            border-radius: 10px;
        """)
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_label)
        
        # Pay button (UI Automation accessible)
        self.pay_button = QPushButton("💳 Ödeme Tamamla")
        self.pay_button.setObjectName("PayButton")  # AutomationId
        self.pay_button.setAccessibleName("PayButton")
        self.pay_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.pay_button.setFixedHeight(70)
        self.pay_button.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #229954;
            }
            QPushButton:pressed {
                background: #1e8449;
            }
            QPushButton:disabled {
                background: #7f8c8d;
            }
        """)
        self.pay_button.clicked.connect(self.complete_payment)
        self.pay_button.setEnabled(False)
        layout.addWidget(self.pay_button)
        
        # Clear cart button
        clear_button = QPushButton("🗑️ Sepeti Temizle")
        clear_button.setFont(QFont("Arial", 12))
        clear_button.setFixedHeight(50)
        clear_button.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #c0392b;
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
        """Create widget for a cart item with UI Automation support"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: #34495e;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Item name (UI Automation accessible)
        name_label = QLabel(item['name'])
        name_label.setObjectName(f"receipt_item_{index}_name")
        name_label.setAccessibleName(f"receipt_item_{index}_name")
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white;")
        layout.addWidget(name_label)
        
        # Price and quantity (UI Automation accessible)
        info_layout = QHBoxLayout()
        
        price_label = QLabel(f"{item['price']}₺")
        price_label.setObjectName(f"receipt_item_{index}_price")
        price_label.setAccessibleName(f"receipt_item_{index}_price")
        price_label.setStyleSheet("color: #ecf0f1;")
        
        quantity_label = QLabel(f"x{item['quantity']}")
        quantity_label.setObjectName(f"receipt_item_{index}_quantity")
        quantity_label.setAccessibleName(f"receipt_item_{index}_quantity")
        quantity_label.setStyleSheet("color: #ecf0f1;")
        
        subtotal_label = QLabel(f"{item['price'] * item['quantity']}₺")
        subtotal_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        subtotal_label.setStyleSheet("color: #2ecc71;")
        
        info_layout.addWidget(price_label)
        info_layout.addWidget(quantity_label)
        info_layout.addStretch()
        info_layout.addWidget(subtotal_label)
        
        layout.addLayout(info_layout)
        
        # Remove button
        remove_btn = QPushButton("❌")
        remove_btn.setFixedSize(30, 30)
        remove_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background: #c0392b;
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
    
    def complete_payment(self):
        """Complete payment and show QR popup"""
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
        
        try:
            # Send to WillPay backend
            print(f"📤 Sending receipt to backend: {BACKEND_URL}/receipts")
            response = requests.post(
                f"{BACKEND_URL}/receipts",
                json=receipt_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Receipt created successfully!")
                
                # Handle both object and array response formats
                if isinstance(result, dict):
                    # Backend returns object (current format)
                    receipt_id = result.get('id')
                    print(f"   Receipt ID: {receipt_id}")
                    print(f"   Store: {result.get('storeName', 'N/A')}")
                    print(f"   Total: {result.get('totalAmount', 0)}₺")
                    print(f"   Items: {len(result.get('items', []))} adet")
                elif isinstance(result, list):
                    # Fallback: Backend returns array [id, user_id, store_name, ...]
                    receipt_id = result[0]
                    print(f"   Receipt ID: {receipt_id}")
                    print(f"   Store: {result[2]}")
                    print(f"   Total: {result[4]}₺")
                else:
                    print(f"❌ Unexpected response format: {type(result)}")
                    return
                
                # Create QR URL for WillPay
                # Format: /receipt/new?amount=XX&store=YY&items=ZZ
                from urllib.parse import quote
                import json
                
                store_name = "Granny's Waffle"
                
                # Items array için JSON oluştur
                items_json = json.dumps([
                    {
                        "name": item['name'],
                        "price": float(item['price']),
                        "quantity": item['quantity'],
                        "category": item['category'].lower()
                    }
                    for item in self.cart
                ])
                
                # URL parametreleri oluştur
                store_encoded = quote(store_name)
                items_encoded = quote(items_json)
                
                # QR URL formatı: http://192.168.1.103:8000/receipt/new?amount=...
                qr_url = f"http://192.168.1.103:8000/receipt/new?amount={total_amount}&store={store_encoded}&items={items_encoded}"
                
                print(f"🎯 QR URL: {qr_url[:100]}...")
                print(f"🎯 Receipt ID: {receipt_id}")
                print(f"🎯 Store Name: {store_name}")
                print(f"🎯 Total Amount: {total_amount}₺")
                print(f"🎯 Items Count: {len(self.cart)}")
                
                # Show QR popup
                display_data = {
                    "items": self.cart,
                    "totalAmount": total_amount
                }
                dialog = QRPopup(qr_url, display_data, self)
                dialog.exec()
                
                # Clear cart after successful payment
                self.clear_cart()
                print("✅ Payment completed successfully!")
                
                # Re-enable pay button (will be disabled again since cart is empty)
                self.pay_button.setText("💳 Ödeme Tamamla")
                
                # 🔓 Unlock payment
                self.is_processing_payment = False
                print("🔓 Payment unlocked")
                
            else:
                print(f"❌ Error creating receipt: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                
                # Re-enable pay button on error
                self.pay_button.setEnabled(True)
                self.pay_button.setText("💳 Ödeme Tamamla")
                
                # 🔓 Unlock payment on error
                self.is_processing_payment = False
                print("🔓 Payment unlocked (error)")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Backend connection error. Make sure backend is running on {BACKEND_URL}")
            print("💡 Check if backend is accessible:")
            print(f"   curl {BACKEND_URL}/health")
            
            # Re-enable pay button on error
            self.pay_button.setEnabled(True)
            self.pay_button.setText("💳 Ödeme Tamamla")
            
            # 🔓 Unlock payment on error
            self.is_processing_payment = False
            print("🔓 Payment unlocked (connection error)")
            
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

