# 🧇 Granny's Waffle - WillPay POS System

Modern Windows POS sistemi - Dijital fiş ve QR entegrasyonu ile sadakat programı desteği.

## 📋 Özellikler

### 🖥️ POS Arayüzü
- **Sol Panel**: Kategorilere göre ürün seçimi (Waffle, Smoothie, Kahve)
- **Sağ Panel**: Dinamik sepet yönetimi ve ödeme
- **UI Automation Desteği**: Tüm elementler AutomationId ile etiketli
- **Modern Tasarım**: PyQt6 ile profesyonel görünüm

### 🎯 QR Fiş Sistemi
- Ödeme tamamlanınca otomatik QR popup
- Backend'de benzersiz token oluşturma (UUID + HMAC-SHA256)
- WillPay mobil app entegrasyonu hazır
- KVKK uyumlu anonim müşteri verisi

### 🔧 Backend API
- **POST /receipts**: Yeni fiş oluştur
- **GET /receipts/<id>**: Fiş detaylarını getir
- **GET /receipts/token/<token>**: QR ile fiş sorgula
- **POST /notify/receipt/<id>**: Mobil bildirim gönder
- SQLite veritabanı ile veri saklama

### 🤖 UI Automation
- Windows UIA ile tam otomasyon desteği
- pywinauto ile test scriptleri
- Sepet verilerini okuyabilme
- Ödeme işlemini otomatikleştirme

## 🚀 Kurulum

### 1. Gereksinimleri Yükle

```bash
pip install -r requirements.txt
```

### 2. Backend'i Başlat

```bash
python backend.py
```

Backend http://localhost:5000 adresinde çalışacak.

### 3. POS UI'yi Başlat

```bash
python pos_ui.py
```

## 📖 Kullanım

### POS Sistemi Kullanımı

1. **Ürün Ekleme**: Sol panelden kategori seçip ürüne tıklayın
2. **Sepet Yönetimi**: Sağ panelde ürünleri görün, miktarları ayarlayın
3. **Ödeme**: "💳 Ödeme Tamamla" butonuna basın
4. **QR Göster**: Popup'da QR kodu müşteriye gösterin
5. **Müşteri Okutma**: WillPay mobil app ile QR okutulsun

### Backend API Kullanımı

#### Yeni Fiş Oluştur

```bash
curl -X POST http://localhost:5000/receipts \
  -H "Content-Type: application/json" \
  -d '{
    "store_name": "Granny'\''s Waffle",
    "items": [
      {"name": "Çikolatalı Waffle", "price": 35, "quantity": 1, "category": "Waffle"},
      {"name": "Türk Kahvesi", "price": 15, "quantity": 2, "category": "Kahve"}
    ],
    "totalAmount": 65
  }'
```

Yanıt:
```json
{
  "success": true,
  "receipt_id": 1,
  "token": "a1b2c3d4-e5f6g7h8",
  "qr_url": "https://willpay.app/receipt?token=a1b2c3d4-e5f6g7h8",
  "created_at": "2025-10-18T10:30:00"
}
```

#### Token ile Fiş Sorgula

```bash
curl http://localhost:5000/receipts/token/a1b2c3d4-e5f6g7h8
```

### UI Automation Test

#### Temel Test

```bash
python ui_automation_test.py
```

#### Simülasyon Modu

```bash
python ui_automation_test.py --simulate
```

Bu mod:
1. POS uygulamasına bağlanır
2. Sepetteki ürünleri okur
3. Toplam tutarı görüntüler
4. Ödeme butonuna tıklar

## 🏗️ Mimari

```
[POS Ödeme Tamamlandı]
          │
          ▼
[PC Popup App] → Sepeti UI'dan alır (UI Automation)
          │
          ▼
POST /receipts → Backend fiş ve token oluşturur
          │
          ▼
QR Popup → Müşteri ekranında gösterilir
          │
          ▼
[Müşteri QR okur] → WillPay mobil app token doğrular
          │
          ▼
Dijital fiş + sadakat puanı mobil app'e düşer
```

## 📊 Veritabanı Şeması

### receipts
- `id`: INTEGER (Primary Key)
- `user_id`: TEXT
- `store_name`: TEXT
- `total_amount`: REAL
- `category`: TEXT
- `date`: TEXT
- `notes`: TEXT
- `token`: TEXT (Unique)
- `created_at`: TEXT

### receipt_items
- `id`: INTEGER (Primary Key)
- `receipt_id`: INTEGER (Foreign Key)
- `name`: TEXT
- `price`: REAL
- `quantity`: INTEGER
- `category`: TEXT
- `created_at`: TEXT

## 🎨 UI Automation Element ID'leri

### Sepet Elementleri
- `receipt_item_0_name`: İlk ürün adı
- `receipt_item_0_price`: İlk ürün fiyatı
- `receipt_item_0_quantity`: İlk ürün miktarı
- `receipt_item_X_...`: Diğer ürünler (X = index)

### Kontrol Elementleri
- `TotalLabel`: Toplam tutar etiketi
- `PayButton`: Ödeme butonu

## 🔐 Güvenlik

- **Token Güvenliği**: HMAC-SHA256 ile imzalı tokenlar
- **HTTPS**: Production'da HTTPS zorunlu
- **KVKK Uyumlu**: Müşteri bilgisi anonim/opsiyonel
- **Rate Limiting**: Production'da eklenebilir

## 🧪 Test Senaryoları

### Manuel Test
1. POS'u çalıştır
2. Sepete 3-4 ürün ekle
3. Ödeme yap
4. QR popup'ı kontrol et
5. Backend log'larını incele

### Automation Test
```bash
# Terminal 1: Backend başlat
python backend.py

# Terminal 2: UI başlat
python pos_ui.py

# Terminal 3: Test çalıştır
python ui_automation_test.py
```

## 📱 WillPay Mobil Entegrasyonu

Mobil uygulama tarafında:

1. QR kodu tara
2. Token'ı backend'e gönder: `GET /receipts/token/{token}`
3. Fiş detaylarını al
4. Kullanıcıya göster ve sadakat puanı ekle
5. Bildirim gönder: `POST /notify/receipt/{receipt_id}`

## 🛠️ Geliştirme Notları

### Yeni Ürün Kategori Ekleme

`pos_ui.py` dosyasında `PRODUCTS` dictionary'sine ekleyin:

```python
PRODUCTS = {
    "YeniKategori": [
        {"name": "Yeni Ürün", "price": 20, "emoji": "🎯"},
    ],
    # ... diğer kategoriler
}
```

### Backend URL Değiştirme

`pos_ui.py` dosyasında:

```python
BACKEND_URL = "https://api.willpay.com"  # Production URL
```

### Token Algoritması Özelleştirme

`backend.py` dosyasında `generate_token()` fonksiyonunu düzenleyin.

## 🐛 Bilinen Sorunlar & Çözümler

### Backend Bağlantı Hatası
**Sorun**: "Backend connection error"
**Çözüm**: Backend'in çalıştığından emin olun (`python backend.py`)

### UI Automation Bulamıyor
**Sorun**: pywinauto elementleri bulamıyor
**Çözüm**: 
- Windows'ta çalıştığınızdan emin olun
- POS uygulaması açık olmalı
- `ui_automation_test.py` içinde `time.sleep()` sürelerini artırın

### QR Kod Gösterilmiyor
**Sorun**: QR popup açılmıyor
**Çözüm**: 
- `qrcode` ve `Pillow` paketlerinin yüklü olduğunu kontrol edin
- Backend'den 201 response geldiğini doğrulayın

## 📄 Lisans

Bu proje WillPay için geliştirilmiş bir PoC (Proof of Concept) uygulamasıdır.

## 👥 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

Sorular için: support@willpay.com

---

**Not**: Bu uygulama Windows platformu için optimize edilmiştir. macOS/Linux'ta UI Automation özellikleri çalışmayabilir.

