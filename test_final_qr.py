#!/usr/bin/env python3
"""
FINAL QR TEST - Kamera için optimum ayarlar
"""

import qrcode

# Test URL - WillPay formatı
url = "http://172.20.10.4:8000/receipt/new?amount=50&store=Grannys"

print("=" * 70)
print("🎯 KAMERA İÇİN OPTIMUM QR KODU")
print("=" * 70)
print(f"URL: {url}")
print(f"Length: {len(url)} chars")
print("=" * 70)

# OPTIMUM AYARLAR - Kamera için
qr = qrcode.QRCode(
    version=None,  # Otomatik
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Yüksek hata düzeltme
    box_size=10,  # Büyük modüller
    border=4  # Standart kenarlık
)

qr.add_data(url)
qr.make(fit=True)

# QR oluştur
img = qr.make_image(fill_color="black", back_color="white")
img.save("FINAL_QR_CAMERA_TEST.png")

print("✅ QR OLUŞTURULDU: FINAL_QR_CAMERA_TEST.png")
print("")
print("📱 KAMERA İLE TEST EDİN:")
print("   - Bu dosyayı açın")
print("   - Ekran parlaklığını maksimuma çıkarın")
print("   - Telefon kamerasını 20cm uzağa tutun")
print("   - 2-3 saniye bekleyin")
print("=" * 70)
print("")
print("Terminal'de QR görünümü:")
qr.print_ascii(invert=True)
print("")
print("=" * 70)
print("AYARLAR:")
print(f"  - Error Correction: HIGH (hasarlı bile okur)")
print(f"  - Box Size: 10 (büyük modüller)")
print(f"  - Border: 4 (standart)")
print(f"  - Version: Otomatik")
print("=" * 70)

