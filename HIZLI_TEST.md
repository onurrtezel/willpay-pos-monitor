# ⚡ 15 Dakikada Test Et

## 🎯 Amaç
POS Monitor'ün çalıştığını test etmek ve QR popup'ı görmek.

---

## 📋 ADIMLAR (15 dk)

### ⏱️ Adım 1: Loyverse İndir (3 dk)

```
https://loyverse.com/download
```

1. "Download for Windows" tıkla
2. İndir ve kur (normal kurulum)
3. Email ile hesap oluştur

---

### ⏱️ Adım 2: Loyverse'te Demo Ürün Ekle (3 dk)

1. **Loyverse'ü aç**
2. **"Ürünler"** menüsüne git
3. **"Yeni Ürün"** tıkla
4. Şunları ekle:
   ```
   Ürün 1: Waffle - 35₺
   Ürün 2: Kahve  - 15₺
   Ürün 3: Çay    - 10₺
   ```

---

### ⏱️ Adım 3: Python Hazırlık (2 dk)

Windows CMD veya PowerShell'de:

```cmd
cd C:\willpay_pos
pip install pywinauto
```

**Kontrol:**
```cmd
python test_windows.py
```

**Çıktı:**
```
✅ pywinauto yüklü
✅ Loyverse POS bulundu
```

---

### ⏱️ Adım 4: POS Monitor Başlat (1 dk)

```cmd
python pos_monitor.py
```

**Pencere açılacak** → "WillPay POS Monitor"

---

### ⏱️ Adım 5: POS'a Bağlan (1 dk)

1. **Loyverse satış ekranı açık olmalı**
2. POS Monitor'de **"🔗 POS'a Bağlan"** tıkla

**Log'da göreceksiniz:**
```
✅ POS bulundu: Loyverse POS
✅ Otomatik bağlanıldı!
```

---

### ⏱️ Adım 6: İzlemeyi Başlat (30 sn)

**"▶️ İzlemeyi Başlat"** butonuna tıkla

**Log:**
```
▶️ İzleme başlatıldı (0.5s)
📊 İlk okuma: 0₺
```

---

### ⏱️ Adım 7: TEST! (3 dk)

#### Loyverse'te:

1. **Waffle** ekle (35₺)
   
   **Log'da:**
   ```
   🔔 DEĞİŞİKLİK! 0₺ → 35₺
      ➕ Ürün eklendi
   ```

2. **Kahve** ekle (15₺)
   
   **Log'da:**
   ```
   🔔 DEĞİŞİKLİK! 35₺ → 50₺
      ➕ Ürün eklendi
   ```

3. **ÖDEME YAP** (Loyverse'te "Pay" butonu)
   
   **Log'da:**
   ```
   💳 ÖDEME TAMAMLANDI!
   📤 Otomatik gönderiliyor...
   ✅ QR gösterildi!
   ```

4. **🎉 QR POPUP AÇILACAK!**

---

## ✅ Başarı Kriterleri

- [ ] Loyverse açık
- [ ] POS Monitor bağlandı
- [ ] Ürün ekleme algılandı
- [ ] Ödeme algılandı
- [ ] **QR popup açıldı** ← ANA HEDEF

---

## 🐛 Sorun mu Var?

### Loyverse Bulunamadı:
```
Log: ❌ POS bulunamadı
```
**Çözüm:** Loyverse'ün pencere başlığını kontrol edin, koda ekleyin.

### Toplam Tutar Okunamıyor:
```
Log: 📊 İlk okuma: None
```
**Çözüm:** `extract_total()` fonksiyonunu Loyverse'e göre ayarlayın.

### Backend'e Gönderilmiyor:
```
Log: ❌ Backend connection error
```
**Çözüm:** Backend'i başlatın veya düzeltin.

---

## 🎯 TEST SONUCU

### ✅ Başarılı:
```
Loyverse'te ödeme yaptım
→ POS Monitor algıladı
→ QR popup açıldı
→ Backend'e fiş gönderildi
```
**SİSTEM ÇALIŞIYOR! 🎉**

### ⚠️ Kısmi Başarılı:
```
Loyverse'e bağlandı
Ürün ekleme algılandı
AMA ödeme algılanmadı
```
**Ödeme algılama kodunu optimize edelim.**

### ❌ Başarısız:
```
Loyverse bulunamadı
```
**Pencere başlığını ekleyelim.**

---

## 💡 HIZLI TEST (Backend Olmadan)

Backend çalışmasa bile test edebilirsiniz:

**Log'da şunları göreceksiniz:**
```
✅ POS bağlandı
🔔 Değişiklikler algılanıyor
❌ Backend connection error (Normal - backend yok)
```

**Bu bile başarıdır!** UI Automation çalışıyor demek.

---

## 🚀 BAŞLAYIN:

```
1. https://loyverse.com/download
2. Kur
3. python pos_monitor.py
4. Test et!
```

**15 dakikada test edin, sonucu söyleyin!** 😊

