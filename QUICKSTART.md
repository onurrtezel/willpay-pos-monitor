# 🚀 Quick Start Guide

## Hızlı Başlangıç (5 dakika)

### 1️⃣ Kurulum

```bash
# Projeyi klonla veya indir
cd granny\'s_waffle_QR

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2️⃣ Backend'i Başlat

**Terminal 1:**
```bash
python backend.py
```

Çıktı:
```
🚀 Initializing WillPay Backend...
✅ Database initialized
🌐 Starting Flask server on http://localhost:5000
```

### 3️⃣ POS UI'yi Başlat

**Terminal 2:**
```bash
python pos_ui.py
```

### 4️⃣ İlk Ödeme

1. Sol panelden ürün seç (örn: Çikolatalı Waffle)
2. Sepete ekle
3. Sağ panelde toplam tutarı gör
4. **"💳 Ödeme Tamamla"** butonuna bas
5. QR popup açılacak! 🎉

---

## 🎯 Tek Komutla Başlat (Otomatik)

### Windows:
```bash
start.bat
```

### macOS/Linux:
```bash
./start.sh
```

Bu scriptler hem backend'i hem UI'yi otomatik başlatır.

---

## 🧪 API Test

Backend çalışıyor mu kontrol et:

```bash
python test_api.py
```

Örnek fişler oluştur:

```bash
python test_api.py --samples
```

---

## 🤖 UI Automation Test

POS UI'yi başlat, sonra:

```bash
python ui_automation_test.py
```

Otomatik ödeme simülasyonu:

```bash
python ui_automation_test.py --simulate
```

---

## 📱 Mobil Entegrasyon Test

### QR Kodu Test Et

1. POS'ta ödeme yap
2. QR popup'ı göster
3. Telefonunla QR'ı tara
4. Backend'de token doğrula:

```bash
curl http://localhost:5000/receipts/token/YOUR_TOKEN
```

---

## 🛠️ Sorun Giderme

### Backend çalışmıyor
```bash
# Port 5000 kullanımda mı kontrol et
lsof -i :5000

# Kill et ve yeniden başlat
kill -9 $(lsof -t -i:5000)
python backend.py
```

### PyQt6 yüklenmiyor
```bash
# Pip'i güncelle
pip install --upgrade pip

# PyQt6'yı manuel yükle
pip install PyQt6
```

### UI Automation çalışmıyor
- **Windows kullanmalısınız** (pywinauto Windows'a özeldir)
- POS uygulaması açık olmalı
- Admin yetkisi gerekebilir

---

## 📊 Proje Yapısı

```
granny's_waffle_QR/
├── backend.py              # Flask API server
├── pos_ui.py              # PyQt6 POS interface
├── ui_automation_test.py  # UI Automation tests
├── test_api.py            # API tests
├── requirements.txt       # Python dependencies
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── start.sh               # Auto-start (Unix)
├── start.bat              # Auto-start (Windows)
└── example_products.json  # Sample product data
```

---

## 💡 Hızlı Özellik Ekleme

### Yeni Ürün Ekle

`pos_ui.py` → `PRODUCTS` dictionary:

```python
"YeniKategori": [
    {"name": "Yeni Ürün", "price": 25, "emoji": "🎯"},
]
```

### Backend URL Değiştir

`pos_ui.py`:

```python
BACKEND_URL = "https://api.willpay.com"
```

### Veritabanı Sıfırla

```bash
rm willpay.db
python backend.py  # Yeni DB oluşturulur
```

---

## 🎓 Öğrenme Kaynakları

1. **Backend API**: `backend.py` dosyasını oku
2. **UI Design**: `pos_ui.py` → `init_ui()` fonksiyonu
3. **QR Generation**: `pos_ui.py` → `QRPopup` class
4. **Automation**: `ui_automation_test.py` → `POSAutomationTester`

---

## 📞 Yardım

Sorun mu yaşıyorsun?

1. README.md'deki "🐛 Bilinen Sorunlar" bölümüne bak
2. Backend log'larını kontrol et
3. UI Automation için Windows kullandığından emin ol

---

**İyi kodlamalar! 🚀**

