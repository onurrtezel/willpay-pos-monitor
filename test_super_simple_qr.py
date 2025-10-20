#!/usr/bin/env python3
"""
SÜPER BASİT QR - Kamera kesinlikle okumalı
"""

import qrcode

# Çok kısa URL
url = "http://172.20.10.4:8000/r?a=50&s=G"

print("=" * 70)
print("🔥 SÜPER BASİT QR - KAMERA KESİNLİKLE OKUMALI")
print("=" * 70)
print(f"URL: {url}")
print(f"Length: {len(url)} chars (ÇOK KISA!)")
print("=" * 70)

# EN BASİT AYARLAR
qr = qrcode.QRCode(
    version=1,  # En küçük
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # En basit
    box_size=12,  # Çok büyük modüller
    border=4
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("SUPER_SIMPLE_QR.png")

print("✅ QR OLUŞTURULDU: SUPER_SIMPLE_QR.png")
print("")
print("📱 BU QR MUTLAKA OKUNMALI:")
print("   ✅ Çok kısa URL (39 karakter)")
print("   ✅ En basit error correction")
print("   ✅ Çok büyük modüller")
print("   ✅ Version 1 (en küçük)")
print("")
print("🧪 TEST:")
print("   1. SUPER_SIMPLE_QR.png dosyasını açın")
print("   2. Kamera ile okuyun")
print("   3. EĞER BU OKUMAZSA → Kameranız QR okuyamıyor!")
print("=" * 70)
print("")
qr.print_ascii(invert=True)
print("")
print("=" * 70)

# Karşılaştırma için eski URL
old_url = "http://172.20.10.4:8000/receipt/new?amount=50&store=Grannys"
print(f"\n📊 KARŞILAŞTIRMA:")
print(f"   Eski URL: {len(old_url)} karakter")
print(f"   Yeni URL: {len(url)} karakter")
print(f"   📉 {len(old_url) - len(url)} karakter DAHA KISA!")
print("=" * 70)

