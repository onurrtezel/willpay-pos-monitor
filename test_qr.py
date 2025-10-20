#!/usr/bin/env python3
"""
Test QR Code Generator
Kameranızla bu QR'ı okuyabilir misiniz test edin
"""

import qrcode
from PIL import Image

# Test URL - aynı format
test_url = "http://172.20.10.4:8000/receipt/new?amount=50&store=Grannys"

print("=" * 60)
print("🔍 QR TEST")
print("=" * 60)
print(f"URL: {test_url}")
print(f"URL Length: {len(test_url)} characters")
print("=" * 60)

# Standart QR ayarları
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
)

qr.add_data(test_url)
qr.make(fit=True)

# QR oluştur
img = qr.make_image(fill_color="black", back_color="white")

# Kaydet
img.save("test_qr.png")

print("✅ QR kod oluşturuldu: test_qr.png")
print("📱 Bu dosyayı açıp kameranızla okuyun!")
print("")
print("Terminal'de göster:")
qr.print_ascii(invert=True)

