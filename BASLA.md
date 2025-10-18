# 🚀 BAŞLANGIÇ REHBERİ

## ✅ NE VAR?

**POS Monitor** - Mevcut POS programınızdan **UI Automation** ile veri çeker.

```
[Mevcut POS (Loyverse/TouchBistro/vb.)]
            ↓
    UI Automation (pywinauto)
            ↓
[POS Monitor] ← BU PROGRAM
            ↓
    WillPay Backend
            ↓
[QR Kod Göster] → Müşteri tarar → Fiş düşer
```

---

## 🪟 WINDOWS'TA KURULUM

### 1. Dosyaları Kopyalayın
```
C:\willpay_pos\
```

### 2. Python ve Bağımlılıklar
```cmd
cd C:\willpay_pos
pip install -r requirements.txt
```

### 3. POS Programı İndirin (Örnek: Loyverse)
```
https://loyverse.com/download
```

Loyverse'ü kurun ve satış ekranını açın.

---

## ⚡ ÇALIŞTIRMA

### Windows'ta:
```cmd
python pos_monitor.py
```

### Adımlar:
1. **🔗 POS'a Bağlan** → Loyverse'ü otomatik bulur
2. **▶️ İzlemeyi Başlat** → Sürekli izler (0.5s)
3. **Ödeme yapın** → QR otomatik açılır

---

## 🎯 NASIL ÇALIŞIR?

### Otomatik Algılama:
```
Program açıldığında "Loyverse" kelimesini arar
→ Bulunca otomatik bağlanır
→ Hazır!
```

### Değişiklik İzleme:
```
Toplam: 0₺ → Sessiz
Toplam: 35₺ → "Ürün eklendi" (log)
Toplam: 50₺ → "Ürün eklendi" (log)
Toplam: 0₺ → "ÖDEME TAMAMLANDI!" → QR AÇILIR
```

---

## 📋 GEREKLİ DOSYALAR

### Ana Program:
- **pos_monitor.py** ⭐ → UI Automation ile POS izleyici

### Test:
- **test_windows.py** → Windows hazırlık testi
- **test_api.py** → Backend testi
- **test_simple.py** → QR format testi

### Dokümantasyon:
- **BASLA.md** → Bu dosya
- **POS_MONITOR_GUIDE.md** → Detaylı kullanım
- **TEST_POS_PROGRAMS.md** → Test programları
- **WINDOWS_DEPLOYMENT.md** → Kurulum rehberi

### Alternatif:
- **pos_ui.py** → Kendi POS'umuz (isteğe bağlı)

---

## 🧪 TEST

### Hazırlık Testi (Windows):
```cmd
python test_windows.py
```

**Göreceksiniz:**
```
✅ pywinauto yüklü
📊 12 pencere bulundu
✅ Loyverse POS bulundu
```

### Ana Program:
```cmd
python pos_monitor.py
```

**Göreceksiniz:**
```
✅ POS bulundu: Loyverse
▶️ İzleme başlatıldı
🔔 Değişiklik algılandı
💳 Ödeme tamamlandı
🎉 QR açıldı!
```

---

## ⚙️ AYARLAR

### Backend URL (pos_monitor.py):
```python
BACKEND_URL = "http://192.168.1.103:8000"
```

### POS Program İsmi Ekleme:
```python
pos_keywords = [
    'Loyverse',
    'SIZIN_POS_PROGRAMINIZ',  # ← Buraya ekleyin
]
```

### Tarama Hızı:
```python
self.scan_timer.start(500)  # 500ms = 0.5 saniye
```

---

## 🎯 ÖZET

**İhtiyacınız Olan:**
- ✅ Windows bilgisayar
- ✅ Python 3.10+
- ✅ Loyverse (veya başka POS)
- ✅ WillPay Backend (çalışır durumda)

**Program:**
- ✅ **pos_monitor.py** ← SADECE BU!

**Çalıştırma:**
```cmd
python pos_monitor.py
```

**O kadar!** 🎉

---

## 📞 YARDIM

**Sorun:** POS bulunamıyor
**Çözüm:** `python test_windows.py` ile kontrol edin

**Sorun:** Backend'e gönderilmiyor
**Çözüm:** Backend'i düzeltin (syntax error var)

**Sorun:** QR açılmıyor
**Çözüm:** Backend çalışınca açılacak

---

**Windows'ta Loyverse + pos_monitor.py = TAMAM!** ✅

