#!/usr/bin/env python3
"""
Basit QR Test - Farklı formatları dene
"""

import qrcode

# Test URL'leri
test_urls = [
    ("Tam URL", "http://172.20.10.4:8000/receipt/new?amount=50&store=Grannys"),
    ("Google", "https://www.google.com"),
    ("Kısa URL", "http://bit.ly/test123"),
]

print("=" * 60)
print("🧪 QR FORMATLARINI TEST ET")
print("=" * 60)

for name, url in test_urls:
    print(f"\n📱 {name}: {url}")
    print(f"   Length: {len(url)} chars")
    
    # QR oluştur
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    filename = f"test_{name.lower().replace(' ', '_')}.png"
    img.save(filename)
    print(f"   ✅ Kaydedildi: {filename}")

print("\n" + "=" * 60)
print("📱 Test edin:")
print("1. test_google.png'i kamera ile okuyun (çalışmalı)")
print("2. test_tam_url.png'i kamera ile okuyun")
print("=" * 60)

