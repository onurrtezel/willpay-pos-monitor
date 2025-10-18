"""
EN BASİT TEST - Backend olmadan QR gösterme
"""
import qrcode
from PIL import Image
from datetime import datetime

print("=" * 60)
print("🧪 Basit QR Test (Backend Gerektirmez)")
print("=" * 60)
print()

# Test verisi
total_amount = 90
receipt_id = "TEST-123"
store_name = "Granny's Waffle"

print(f"📝 Test Fiş:")
print(f"   Store: {store_name}")
print(f"   Tutar: {total_amount}₺")
print(f"   ID: {receipt_id}")
print()

# QR URL oluştur
import json
from urllib.parse import quote

items = [
    {"name": "Çikolatalı Waffle", "price": 35, "quantity": 1, "category": "waffle"},
    {"name": "Türk Kahvesi", "price": 15, "quantity": 1, "category": "kahve"}
]

items_json = json.dumps(items)
qr_url = f"http://192.168.1.103:8000/receipt/new?amount={total_amount}&store={quote(store_name)}&items={quote(items_json)}"

print("🎯 QR İçeriği:")
print(f"   {qr_url}")
print()

# QR kod oluştur
print("📱 QR kod oluşturuluyor...")
qr = qrcode.QRCode(version=1, box_size=10, border=2)
qr.add_data(qr_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# QR'ı kaydet
qr_filename = "test_qr.png"
img.save(qr_filename)
print(f"✅ QR kod kaydedildi: {qr_filename}")
print()

# QR'ı göster
try:
    img.show()
    print("🖼️ QR kod görüntüleyicide açıldı!")
except:
    print("⚠️ QR otomatik açılamadı, manuel açın: test_qr.png")

print()
print("=" * 60)
print("✅ Test başarılı!")
print()
print("💡 test_qr.png dosyasını telefonla tarayın")
print("   Backend çalışıyorsa fiş eklenecek!")
print("=" * 60)

