# 🔌 WillPay Backend Entegrasyonu

## ✅ Entegrasyon Tamamlandı!

Bu POS sistemi mevcut **WillPay Backend**'inize başarıyla entegre edilmiştir.

---

## 🌐 Backend Yapılandırması

### Aktif Backend Adresi
```
http://192.168.1.103:8000
```

### Kullanılan Endpoint'ler

#### 1. Health Check
```bash
GET http://192.168.1.103:8000/health
```

#### 2. Receipt Oluşturma
```bash
POST http://192.168.1.103:8000/receipts
```

**Request Format:**
```json
{
  "user_id": 1,
  "store_name": "Granny's Waffle",
  "date": "2025-10-18",
  "total_amount": 100.0,
  "category": "food",
  "is_favorite": false,
  "notes": "POS Payment - Granny's Waffle",
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

**Response Format:**
```json
[
  104,                                    // id
  1,                                      // user_id
  "Granny's Waffle",                     // store_name
  "Sat, 18 Oct 2025 00:00:00 GMT",      // date
  "100.00",                              // total_amount
  "food",                                // category
  false,                                 // is_favorite
  "POS Payment",                         // notes
  null,                                  // image_url
  "Sat, 18 Oct 2025 14:02:06 GMT"       // created_at
]
```

#### 3. Receipt Sorgulama (QR Scan)
```bash
GET http://192.168.1.103:8000/receipts/{receipt_id}
```

**Response:**
```json
{
  "id": 105,
  "store_name": "Granny's Waffle",
  "total_amount": 100.0,
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

---

## 🎯 QR Kod Formatı

POS sisteminden oluşturulan QR kodlar şu formattadır:

```
http://192.168.1.103:8000/receipt/{receipt_id}
```

**Örnek:**
```
http://192.168.1.103:8000/receipt/105
```

Bu URL WillPay mobil uygulaması tarafından taranabilir.

---

## 🔧 Yapılandırma Değişiklikleri

### Backend URL'i Değiştirme

#### 1. POS UI (`pos_ui.py`)

```python
# Satır 40-42
BACKEND_URL = "http://192.168.1.103:8000"  # Mevcut WillPay Backend
# BACKEND_URL = "http://localhost:8000"  # Localhost için
```

#### 2. Test Script (`test_api.py`)

```python
# Satır 9-11
BACKEND_URL = "http://192.168.1.103:8000"  # Mevcut WillPay Backend
# BACKEND_URL = "http://localhost:8000"  # Localhost için
```

---

## 🧪 Test Senaryoları

### 1. Backend Bağlantı Testi

```bash
curl http://192.168.1.103:8000/health
```

**Beklenen:**
```json
{
  "message": "WillPay API is running",
  "status": "healthy"
}
```

### 2. Receipt Oluşturma Testi

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

### 3. Örnek Fişler Oluşturma

```bash
python test_api.py --samples
```

Bu komut 3 farklı büyüklükte örnek fiş oluşturur:
- **Small Order**: Türk Kahvesi (15₺)
- **Medium Order**: Waffle + Cappuccino (55₺)
- **Large Order**: 2x Waffle + 3x Smoothie + 2x Latte (189₺)

---

## 📱 POS Kullanımı

### Adım 1: POS'u Başlat

```bash
python pos_ui.py
```

### Adım 2: Ürün Ekle

1. Sol panelden kategori seç (Waffle, Smoothie, Kahve)
2. Ürüne tıkla
3. Sepete eklendiğini gör

### Adım 3: Ödeme

1. Sağ panelde sepeti kontrol et
2. **"💳 Ödeme Tamamla"** butonuna bas
3. Backend'e otomatik POST gönderilir

### Adım 4: QR Göster

1. Popup açılır ve QR kodu gösterilir
2. Müşteri WillPay app ile QR'ı tarar
3. Dijital fiş mobil uygulamaya düşer

---

## 🔍 Debug ve Sorun Giderme

### Backend'e Erişim Kontrol

```bash
# Health check
curl http://192.168.1.103:8000/health

# Network üzerinden erişim
ping 192.168.1.103

# Port kontrolü
nc -zv 192.168.1.103 8000
```

### POS Logları

POS çalıştırıldığında terminal'de log mesajları görünür:

```
📤 Sending receipt to backend: http://192.168.1.103:8000/receipts
✅ Receipt created: [106, 1, "Granny's Waffle", ...]
✅ Payment completed successfully!
```

### Hata Mesajları

#### Backend Bağlantı Hatası
```
❌ Backend connection error. Make sure backend is running on http://192.168.1.103:8000
💡 Check if backend is accessible:
   curl http://192.168.1.103:8000/health
```

**Çözüm:**
- Backend'in çalıştığından emin olun
- Network bağlantısını kontrol edin
- Firewall ayarlarını kontrol edin

#### Invalid Response Format
```
❌ Unexpected response format: <class 'str'>
```

**Çözüm:**
- Backend'in doğru JSON dönüp dönmediğini kontrol edin
- Response formatının array veya object olduğundan emin olun

---

## 🚀 Production Deployment

### 1. Backend URL'i Güncelle

Production backend'i kullanmak için:

```python
# pos_ui.py
BACKEND_URL = "https://api.willpay.com"  # Production URL
```

### 2. HTTPS Kullan

Production'da mutlaka HTTPS kullanın:

```python
qr_url = f"https://api.willpay.com/receipt/{receipt_id}"
```

### 3. User ID Yönetimi

Şu anda sabit `user_id: 1` kullanılıyor. Production'da:

```python
# Dinamik user_id kullanın
receipt_data = {
    "user_id": current_user_id,  # Login sisteminden alın
    # ...
}
```

### 4. Error Handling

Production'da daha kapsamlı error handling ekleyin:

```python
try:
    response = requests.post(...)
    if response.status_code in [200, 201]:
        # Success
    else:
        # Log error
        logger.error(f"Receipt creation failed: {response.text}")
        # Show user-friendly message
        show_error_dialog("Ödeme işlemi başarısız. Lütfen tekrar deneyin.")
except Exception as e:
    logger.exception("Payment error")
    show_error_dialog(f"Bir hata oluştu: {str(e)}")
```

---

## 📊 Backend İstatistikleri

### Oluşturulan Fişler

Backend'deki tüm fişleri görmek için:

```bash
curl http://192.168.1.103:8000/receipts | python -m json.tool
```

### Belirli Fiş Detayı

```bash
curl http://192.168.1.103:8000/receipts/105 | python -m json.tool
```

---

## 🔄 Veri Formatı Dönüşümü

POS sistemi backend'in array formatını otomatik olarak handle eder:

### Backend Array Response → Dict Conversion

```python
# Backend dönüşü (array)
[104, 1, "Granny's Waffle", "2025-10-18", "100.00", "food", false, "notes", null, "2025-10-18T14:02:06"]

# POS tarafında dönüştürülür (dict)
{
  'id': 104,
  'user_id': 1,
  'store_name': "Granny's Waffle",
  'date': "2025-10-18",
  'total_amount': 100.0,
  'category': "food",
  'is_favorite': false,
  'notes': "notes",
  'image_url': null,
  'created_at': "2025-10-18T14:02:06"
}
```

---

## ✅ Entegrasyon Checklist

- [x] Backend health check çalışıyor
- [x] Receipt oluşturma başarılı
- [x] Receipt sorgulama çalışıyor (QR scan)
- [x] Items backend'e gönderiliyor
- [x] QR popup gösteriliyor
- [x] Array response formatı handle ediliyor
- [x] Error handling mevcut
- [x] Test scriptleri hazır

---

## 🎉 Sonuç

POS sistemi WillPay backend'inize **tamamen entegre edilmiştir** ve kullanıma hazırdır!

**Test için:**
```bash
python pos_ui.py
```

**Sorular için:**
Bu dokümandaki bilgileri kullanarak sistemi test edebilirsiniz. Herhangi bir sorun olursa debug bölümüne bakın.

