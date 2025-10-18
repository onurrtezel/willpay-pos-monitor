# 🧇 Granny's Waffle - WillPay POS Sistemi

**✅ WillPay Backend Entegrasyonu Tamamlandı!**

Modern Windows POS sistemi - Mevcut WillPay Backend'inize entegre, dijital fiş ve QR desteği ile.

---

## 🚀 Hızlı Başlangıç

### 1. POS'u Başlat

```bash
python pos_ui.py
```

### 2. Ürün Ekle ve Ödeme Yap

1. Sol panelden ürün seç (Waffle, Smoothie, Kahve)
2. Sepete ekle
3. **"💳 Ödeme Tamamla"** butonuna bas
4. QR popup açılır ve müşteri tarayabilir!

---

## 🌐 Backend Yapılandırması

### Aktif Backend
```
http://192.168.1.103:8000
```

Bu adres `pos_ui.py` dosyasında tanımlıdır. Değiştirmek için:

```python
# Satır 40-42
BACKEND_URL = "http://192.168.1.103:8000"
```

---

## 📋 Özellikler

### ✅ Ekran Arayüzü
- **Sol Panel**: Kategorilere göre ürün listesi (Waffle, Smoothie, Kahve)
- **Sağ Panel**: Dinamik sepet + toplam tutar
- **Modern UI**: PyQt6 ile profesyonel tasarım
- **UI Automation**: Tüm elementler AutomationId ile etiketli

### ✅ QR Fiş Sistemi
- Ödeme sonrası otomatik QR popup
- WillPay backend'e gerçek zamanlı POST
- Mobil app entegrasyonu hazır
- Format: `http://192.168.1.103:8000/receipt/{receipt_id}`

### ✅ Backend Entegrasyonu
- **POST /receipts**: Yeni fiş oluşturma ✓
- **GET /receipts/{id}**: Fiş sorgulama ✓
- Array ve Object response formatlarını destekler
- Otomatik error handling

### ✅ UI Automation Desteği
- Windows UIA uyumlu
- pywinauto test scriptleri
- Deterministic elementler
- AutomationId'ler: `TotalLabel`, `PayButton`, `receipt_item_X_name`

---

## 🧪 Test

### Backend Bağlantı Testi

```bash
python test_api.py
```

**Çıktı:**
```
✅ Health check passed
✅ Receipt created successfully
   Receipt ID: 105
   Store: Granny's Waffle
   Total: 100.0₺
✅ QR scan successful
```

### Örnek Fişler Oluştur

```bash
python test_api.py --samples
```

3 farklı büyüklükte örnek fiş oluşturur (15₺, 55₺, 189₺)

### UI Automation Test (Windows)

```bash
python ui_automation_test.py
```

---

## 📦 Kurulum

### Gereksinimler

```bash
pip install -r requirements.txt
```

### Bağımlılıklar

- **PyQt6**: Modern UI framework
- **qrcode**: QR kod üretimi
- **requests**: Backend iletişimi
- **pywinauto**: UI Automation (Windows)

---

## 🎯 Kullanım Senaryosu

```
┌─────────────────────────────────────────────┐
│  1. Müşteri gelir                          │
│  2. Kasiyerler ürün ekler                  │
│  3. "Ödeme Tamamla" butonuna basar         │
│  4. Backend'e POST: /receipts              │
│  5. QR popup açılır                        │
│  6. Müşteri QR'ı tarar                     │
│  7. WillPay app fişi gösterir              │
│  8. Sadakat puanı eklenir                  │
└─────────────────────────────────────────────┘
```

---

## 🔧 Yapılandırma

### Backend URL Değiştirme

**Production için:**
```python
# pos_ui.py
BACKEND_URL = "https://api.willpay.com"
```

**Localhost için:**
```python
BACKEND_URL = "http://localhost:8000"
```

### User ID Yönetimi

Şu anda sabit `user_id: 1` kullanılıyor. Dinamik yapmak için:

```python
# pos_ui.py, complete_payment() fonksiyonu
receipt_data = {
    "user_id": current_cashier_id,  # Login sisteminden
    # ...
}
```

---

## 📱 QR Kod Formatı

```
http://192.168.1.103:8000/receipt/{receipt_id}
```

**Örnek:**
```
http://192.168.1.103:8000/receipt/105
```

Bu URL:
- WillPay mobil app tarafından taranabilir
- Backend'den fiş detaylarını getirir
- Kullanıcıya dijital fiş olarak gösterilir

---

## 🐛 Sorun Giderme

### Backend Bağlanamıyor

```bash
# Backend kontrol
curl http://192.168.1.103:8000/health

# Beklenen çıktı:
{
  "message": "WillPay API is running",
  "status": "healthy"
}
```

**Çözüm:**
1. Backend'in çalıştığından emin olun
2. Network bağlantısını kontrol edin
3. Firewall ayarlarını kontrol edin

### QR Gösterilmiyor

**Çözüm:**
1. `qrcode` ve `Pillow` paketlerinin yüklü olduğunu kontrol edin:
   ```bash
   pip install qrcode Pillow
   ```
2. Backend'den 200/201 response geldiğini doğrulayın

### UI Automation Çalışmıyor

**Not:** UI Automation sadece Windows'ta çalışır!

**Çözüm:**
1. Windows kullandığınızdan emin olun
2. POS uygulaması açık olmalı
3. Admin yetkisiyle çalıştırın

---

## 📊 Backend Veri Formatı

### POST Request

```json
{
  "user_id": 1,
  "store_name": "Granny's Waffle",
  "date": "2025-10-18",
  "total_amount": 100.0,
  "category": "food",
  "is_favorite": false,
  "notes": "POS Payment",
  "image_url": null,
  "items": [
    {
      "name": "Çikolatalı Waffle",
      "price": 35.0,
      "quantity": 1,
      "category": "waffle"
    }
  ]
}
```

### Response (Array Format)

```json
[
  105,                                    // id
  1,                                      // user_id
  "Granny's Waffle",                     // store_name
  "Sat, 18 Oct 2025 00:00:00 GMT",      // date
  "100.00",                              // total_amount (string)
  "food",                                // category
  false,                                 // is_favorite
  "POS Payment",                         // notes
  null,                                  // image_url
  "Sat, 18 Oct 2025 14:02:06 GMT"       // created_at
]
```

**Not:** POS sistemi bu array formatını otomatik olarak handle eder.

---

## 📁 Proje Yapısı

```
granny's_waffle_QR/
├── pos_ui.py              # 🖥️  Ana POS arayüzü (PyQt6)
├── backend.py             # 🔧 Standalone backend (kullanılmıyor)
├── test_api.py            # 🧪 Backend test scripti
├── ui_automation_test.py  # 🤖 UI Automation testi
├── requirements.txt       # 📦 Python bağımlılıkları
├── README.md              # 📚 Bu dosya
├── INTEGRATION.md         # 🔌 Detaylı entegrasyon kılavuzu
├── QUICKSTART.md          # 🚀 Hızlı başlangıç rehberi
├── example_products.json  # 📋 Örnek ürün veritabanı
├── start.sh               # 🐧 Unix başlatma scripti
└── start.bat              # 🪟 Windows başlatma scripti
```

---

## 🎨 Ekran Görünümü

```
┌─────────────────────────────────────────────────────┐
│  🧇 Granny's Waffle - POS System                   │
├──────────────────────┬──────────────────────────────┤
│                      │  🛒 Sepet                    │
│  📂 Waffle          │                              │
│  ┌────────┐┌────────┐│  Çikolatalı Waffle  35₺ x1  │
│  │🍫      ││🍌      ││  Karışık Smoothie   25₺ x2  │
│  │Çikolat ││Muzlu   ││  Türk Kahvesi       15₺ x1  │
│  │35₺     ││30₺     ││                              │
│  └────────┘└────────┘│  ─────────────────────────── │
│                      │  Toplam: 100₺                │
│  📂 Smoothie        │                              │
│  ┌────────┐┌────────┐│  [💳 Ödeme Tamamla]          │
│  │🥤      ││🍓      ││  [🗑️  Sepeti Temizle]        │
│  │Karışık ││Çilekli ││                              │
│  │25₺     ││22₺     ││                              │
│  └────────┘└────────┘│                              │
│                      │                              │
│  📂 Kahve           │                              │
│  ┌────────┐┌────────┐│                              │
│  │☕      ││☕      ││                              │
│  │Türk    ││Espresso││                              │
│  │15₺     ││18₺     ││                              │
│  └────────┘└────────┘│                              │
└──────────────────────┴──────────────────────────────┘
```

---

## 📈 Test Sonuçları

### ✅ Başarılı Testler

```
✅ Backend health check
✅ Receipt oluşturma (ID: 105, 109, 110, 111)
✅ Receipt sorgulama (GET /receipts/{id})
✅ Items backend'e gönderiliyor
✅ QR kod üretimi
✅ Array response formatı
✅ Error handling
```

### 📊 Oluşturulan Örnek Fişler

| ID  | Type         | Items                                   | Total  |
|-----|--------------|-----------------------------------------|--------|
| 109 | Small Order  | Türk Kahvesi x1                        | 15₺    |
| 110 | Medium Order | Waffle x1 + Cappuccino x1              | 55₺    |
| 111 | Large Order  | Waffle x2 + Smoothie x3 + Latte x2     | 189₺   |

---

## 🚀 Production Hazırlığı

### 1. HTTPS Kullanın

```python
BACKEND_URL = "https://api.willpay.com"
```

### 2. Environment Variables

```python
import os
BACKEND_URL = os.getenv('WILLPAY_BACKEND_URL', 'http://localhost:8000')
```

### 3. Logging Ekleyin

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Receipt created: {receipt_id}")
logger.error(f"Backend error: {response.text}")
```

### 4. Retry Mekanizması

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)
```

---

## 📞 Yardım ve Destek

### Dokümantasyon

- **README.md**: Bu dosya (genel bakış)
- **INTEGRATION.md**: Detaylı backend entegrasyonu
- **QUICKSTART.md**: 5 dakikada başlangıç

### Test Komutları

```bash
# Backend test
python test_api.py

# Örnek fişler
python test_api.py --samples

# UI Automation (Windows)
python ui_automation_test.py
```

### Backend Kontrol

```bash
# Health check
curl http://192.168.1.103:8000/health

# Tüm fişler
curl http://192.168.1.103:8000/receipts

# Belirli fiş
curl http://192.168.1.103:8000/receipts/105
```

---

## ✅ Entegrasyon Özeti

| Özellik                    | Durum | Notlar                              |
|----------------------------|-------|-------------------------------------|
| Backend Bağlantısı         | ✅    | http://192.168.1.103:8000          |
| Receipt Oluşturma          | ✅    | POST /receipts                     |
| QR Kod Üretimi             | ✅    | qrcode library                     |
| Receipt Sorgulama          | ✅    | GET /receipts/{id}                 |
| Items Gönderimi            | ✅    | JSON array                         |
| Array Response Handling    | ✅    | Otomatik dönüşüm                   |
| UI Automation              | ✅    | Windows UIA (pywinauto)            |
| Error Handling             | ✅    | Try/catch + user messages          |
| Test Coverage              | ✅    | test_api.py + samples              |

---

## 🎉 Sonuç

**POS Sistemi Hazır!**

- ✅ WillPay backend'inize tam entegre
- ✅ Gerçek zamanlı fiş oluşturma
- ✅ QR kod desteği
- ✅ Mobil app uyumlu
- ✅ Test edilmiş ve çalışıyor

**Başlatmak için:**
```bash
python pos_ui.py
```

**İyi satışlar! 🧇☕🥤**

---

## 📄 Lisans

Bu proje WillPay için geliştirilmiş bir POS entegrasyonudur.

## 🤝 Katkıda Bulunma

1. Backend URL'ini ihtiyacınıza göre ayarlayın
2. Ürün listesini güncelleyin (PRODUCTS dictionary)
3. UI tasarımını özelleştirin
4. Test edin ve geri bildirim verin

---

**Not:** macOS'ta çalıştırıyorsunuz. UI Automation özellikleri sadece Windows'ta çalışır. POS UI ve backend entegrasyonu tüm platformlarda çalışır.

