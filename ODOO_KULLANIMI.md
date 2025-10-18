# 🎯 Odoo POS Kullanım Rehberi

## 📦 Odoo İndirdiniz, Şimdi Ne Yapacaksınız?

---

## 1️⃣ ODOO KURULUM (Windows)

### İndirme:
```
https://www.odoo.com/page/download
→ Community Edition
→ Windows (.exe) seçin
```

### Kurulum:
```
1. odoo_xxx.exe çalıştır
2. Kurulum sihirbazını takip et
3. PostgreSQL otomatik kurulur
4. 10 dakika bekle
5. Browser otomatik açılır: http://localhost:8069
```

---

## 2️⃣ İLK YAPILANDIRMA

### Database Oluştur:
```
1. Master password: admin (varsayılan)
2. Database name: willpay_test
3. Email: sizin@email.com
4. Password: güçlü bir şifre
5. Language: Türkçe
6. "Create database" → Demo data ile ✅
```

### POS Modülünü Aktif Et:
```
1. Odoo ana ekran → Apps
2. Arama: "Point of Sale"
3. "Install" butonu
4. 2 dakika bekle
```

---

## 3️⃣ DEMO ÜRÜNLER EKLE

### Hızlı Yol (Demo Data Varsa):
```
1. Point of Sale → Products
2. Demo ürünler zaten var!
3. Direkt kullanabilirsiniz
```

### Manuel Ürün Ekleme:
```
1. Point of Sale → Products → Create
2. Ürün bilgileri:
   - Name: Çikolatalı Waffle
   - Sales Price: 35
   - Available in POS: ✅
3. Save
4. Diğer ürünler için tekrarla
```

---

## 4️⃣ POS EKRANINI AÇ

### Yöntem 1: Dashboard'tan
```
1. Ana ekran → Point of Sale
2. "New Session" → "Open Session"
3. POS ekranı açılır (tam ekran)
```

### Yöntem 2: Direkt URL
```
http://localhost:8069/pos/web
```

**POS Ekranı:**
```
┌────────────────────────────────────┐
│  Odoo - Point of Sale             │
├─────────────────┬──────────────────┤
│  ÜRÜNLER        │  SEP İT          │
│  ┌──────┐       │  Çikolatalı Waffle│
│  │Waffle│       │  35₺             │
│  │35₺   │       │                  │
│  └──────┘       │  Toplam: 35₺     │
│                 │                  │
│  [Ödeme]        │  [Validate]      │
└─────────────────┴──────────────────┘
```

---

## 5️⃣ POS MONITOR İLE ENTEGRASYON

### Odoo POS + pos_monitor.py:

```cmd
cd C:\willpay_pos
python pos_monitor.py
```

**Log'da:**
```
[12:30:02] 🚀 Otomatik başlatma aktif...
[12:30:03] 🔍 POS aranıyor...
[12:30:03] ✅ POS bulundu: Odoo
[12:30:03] ✅ Otomatik bağlanıldı!
[12:30:04] ▶️ İzleme başlatıldı!
[12:30:04] 📊 İlk okuma: 0₺
```

---

## 6️⃣ TEST SENARYOSU

### Odoo POS'ta:

```
1. "Çikolatalı Waffle" tıkla
   → POS Monitor: "🔔 0₺ → 35₺ (Ürün eklendi)"

2. "Türk Kahvesi" tıkla
   → POS Monitor: "🔔 35₺ → 50₺ (Ürün eklendi)"

3. "Payment" butonu
   → Ödeme ekranı açılır

4. "Validate" butonu
   → Ödeme tamamlanır
   → Odoo ekranı sıfırlanır
   → POS Monitor: "💳 ÖDEME TAMAMLANDI!"
   → QR POPUP AÇILIR! 🎉
```

---

## 🔧 ODOO POS AYARLARI

### POS Yapılandırması:

```
1. Point of Sale → Configuration → Point of Sale
2. "Create" yeni POS
3. Ayarlar:
   - POS Name: Granny's Waffle POS
   - Available Products: Tümü
   - Receipt: Header/Footer ekle
4. Save
```

---

## 💡 ODOO İPUÇLARI

### Hızlı Erişim:
```
http://localhost:8069/pos/web
→ Bookmark'lara ekleyin
```

### Tam Ekran Mod:
```
POS ekranında: F11
→ Tam ekran POS (gerçek kasa gibi)
```

### Ürün Kategori:
```
Point of Sale → Products → Product Categories
→ Waffle, Smoothie, Kahve kategorileri oluştur
```

---

## 🎯 pos_monitor.py İÇİN ÖZEL AYAR

Odoo'nun pencere adını koda ekleyin:

`pos_monitor.py` satır 262:

```python
pos_keywords = [
    'Loyverse', 'Square',
    'Odoo',        # ← Ekleyin
    'odoo',        # ← Küçük harfle de
    'Point of Sale',  # ← Bu da olabilir
]
```

---

## 📊 BEKLENEN AKIŞ

```
╔════════════════════════════════════════╗
║  1. Odoo POS açık (localhost:8069)    ║
╠════════════════════════════════════════╣
║  2. pos_monitor.py başlat             ║
║     → Otomatik Odoo'yu bulur          ║
║     → Otomatik izlemeyi başlatır      ║
╠════════════════════════════════════════╣
║  3. Müşteri gelir                     ║
║     → Kasiyer ürün ekler (Odoo'da)   ║
║     → Monitor algılar (log'da)        ║
╠════════════════════════════════════════╣
║  4. Kasiyer ödeme yapar (Odoo'da)     ║
║     → Monitor algılar                 ║
║     → Backend'e gönderir              ║
║     → QR POPUP AÇAR! 🎉              ║
╠════════════════════════════════════════╣
║  5. Müşteri QR tarar                  ║
║     → WillPay app'te fiş görünür      ║
╚════════════════════════════════════════╝
```

---

## ✅ KONTROL LİSTESİ

**Odoo Kurulumu:**
- [ ] Odoo indirildi
- [ ] Kurulum tamamlandı
- [ ] Database oluşturuldu
- [ ] POS modülü kuruldu
- [ ] Demo ürünler var
- [ ] POS ekranı açılıyor

**POS Monitor:**
- [ ] willpay_pos.zip transfer edildi
- [ ] C:\willpay_pos\ çıkarıldı
- [ ] Python kuruldu
- [ ] pip install -r requirements.txt
- [ ] python pos_monitor.py çalışıyor
- [ ] Odoo'ya bağlandı
- [ ] İzleme başladı

**Test:**
- [ ] Ürün ekleme algılanıyor
- [ ] Ödeme algılanıyor
- [ ] Backend'e gönderiliyor
- [ ] QR popup açılıyor

---

## 🎉 BAŞARI!

Odoo + POS Monitor = Mükemmel eşleşme!

**Odoo kurulunca testi yapın!** 🚀

