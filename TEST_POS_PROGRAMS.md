# 🧪 Test İçin Ücretsiz POS Programları

## ✅ ÖNERİLEN: Loyverse POS

### Neden Loyverse?
- ✅ **Tamamen ücretsiz**
- ✅ **Windows destekliyor**
- ✅ **Restaurant modülü var**
- ✅ **Kolay kurulum**
- ✅ **Türkçe dil desteği**
- ✅ **UI elementleri erişilebilir**

### İndirme:
```
https://loyverse.com/download
```

### Kurulum Adımları:

1. **İndir ve Kur:**
   - Windows için indir
   - Normal kurulum (tıkla-tıkla-bitti)
   - Hesap oluştur (email ile)

2. **Demo Ürünler Ekle:**
   - "Ürünler" → "Yeni Ürün"
   - Waffle (35₺)
   - Kahve (15₺)
   - Smoothie (25₺)

3. **Satış Ekranını Aç:**
   - Ana ekranda "Satış" butonu
   - Ürünlere tıkla
   - Sepete ekle
   - "Ödeme" butonuna bas

---

## 🎯 Test Senaryosu

### Adım 1: Loyverse'ü Aç
```
Loyverse POS → Satış ekranı açık olmalı
```

### Adım 2: POS Monitor'ü Çalıştır
```cmd
cd C:\willpay_pos
python pos_monitor.py
```

### Adım 3: Bağlan
```
"🔗 POS'a Bağlan" → Loyverse'ü otomatik bulacak
```

**Log'da göreceksiniz:**
```
✅ POS bulundu: Loyverse POS
✅ Otomatik bağlanıldı!
```

### Adım 4: İzlemeyi Başlat
```
"▶️ İzlemeyi Başlat"
```

### Adım 5: Loyverse'te Ürün Ekle
```
Loyverse'te:
1. Waffle ekle (35₺)
2. Kahve ekle (15₺)
```

**Log'da göreceksiniz:**
```
[12:30:20] 🔔 DEĞİŞİKLİK! 0₺ → 35₺
[12:30:25] 🔔 DEĞİŞİKLİK! 35₺ → 50₺
```

### Adım 6: Ödeme Yap
```
Loyverse'te "Ödeme" butonuna bas
Ödemeyi tamamla
```

**QR POPUP AÇILACAK! 🎉**

```
[12:30:45] 💳 ÖDEME TAMAMLANDI!
[12:30:46] 📤 Backend'e gönderiliyor...
[12:30:47] ✅ QR gösterildi!
```

---

## 🎨 Alternatif Programlar

### 1. Square POS (Demo Mode)
```
https://squareup.com/us/en/point-of-sale
```
- ✅ Ücretsiz demo
- ✅ Web-based (browser'da)
- ⚠️ UI Automation biraz zor

### 2. Toast POS (Trial)
```
https://pos.toasttab.com/
```
- ✅ 30 gün ücretsiz
- ✅ Restaurant özellikli
- ⚠️ Kayıt gerektirir

### 3. LightSpeed Restaurant (Trial)
```
https://www.lightspeedhq.com/pos/restaurant/
```
- ✅ 14 gün ücretsiz
- ✅ Profesyonel
- ⚠️ Karmaşık kurulum

### 4. ERPNext POS (Açık Kaynak)
```
https://erpnext.com/
```
- ✅ Tamamen ücretsiz
- ✅ Açık kaynak
- ⚠️ Kurulum biraz teknik

---

## 🏆 EN KOLAY TEST: Loyverse

**Neden Loyverse?**

1. **5 dakikada kurulum**
2. **Kayıt ücretsiz** (email yeterli)
3. **Türkçe arayüz**
4. **Demo ürünlerle geliyor**
5. **Windows app** (UI Automation uyumlu)

---

## 📋 Test Checklist

### Hazırlık:
- [ ] Windows bilgisayar
- [ ] Loyverse POS indir ve kur
- [ ] Demo ürünler ekle
- [ ] Python ve bağımlılıklar yüklü

### Test:
- [ ] Loyverse satış ekranı açık
- [ ] `python pos_monitor.py` çalıştır
- [ ] "🔗 POS'a Bağlan" → Loyverse bulundu mu?
- [ ] "▶️ İzlemeyi Başlat"
- [ ] Loyverse'te ürün ekle → Log'da değişiklik görünüyor mu?
- [ ] Loyverse'te ödeme yap → **QR popup açıldı mı?** 🎯

---

## 🎯 Beklenen Sonuç:

```
✅ Loyverse POS açık
✅ POS Monitor bağlandı
✅ Değişiklikleri algılıyor
✅ Ödeme yapılınca QR açılıyor
✅ Backend'e fiş gönderiliyor
```

---

## 💡 POS Monitor Hata Ayıklama

Eğer Loyverse'ü bulmazsa:

```python
# pos_monitor.py içinde pos_keywords'e ekleyin:
pos_keywords = [
    'Loyverse',  # ← BUNU EKLEYİN
    'POS', 'Restaurant',
    # ...
]
```

---

## 📱 Komple Test Akışı

```
1. Loyverse POS indir (5 dk)
   https://loyverse.com/download

2. Hesap oluştur ve giriş yap (2 dk)

3. Demo ürün ekle (3 dk)
   - Waffle 35₺
   - Kahve 15₺

4. POS Monitor başlat (1 dk)
   python pos_monitor.py

5. Bağlan ve izle (1 dk)
   🔗 POS'a Bağlan → ▶️ İzlemeyi Başlat

6. Test et (2 dk)
   Loyverse'te: Ürün ekle → Ödeme yap

7. QR göründü mü? 🎉
```

**Toplam süre: ~15 dakika**

---

## 🚀 Hemen Başlayın:

```
1. https://loyverse.com/download
2. İndirin ve kurun
3. python pos_monitor.py
4. Test edin!
```

**Sonucu bana söyleyin, gerekirse kod ayarları yaparız!** 😊

