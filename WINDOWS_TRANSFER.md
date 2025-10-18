# 🪟 Windows Bilgisayara Transfer Rehberi

## 📦 macOS'tan Windows'a Dosya Transferi

---

## 1️⃣ DOSYALARI HAZIRLA (macOS - Şimdi)

### Gereksiz dosyaları temizle:

```bash
cd '/Users/onurtezel/granny'"'"'s_waffle_QR'

# venv ve cache'i sil (Windows'ta yeniden oluşturulacak)
rm -rf venv
rm -rf __pycache__
rm -f *.pyc
rm -f test_qr.png
rm -f willpay.db
```

### Dosyaları zip'le:

```bash
cd ..
zip -r willpay_pos.zip granny\'s_waffle_QR/
```

**Sonuç:** `willpay_pos.zip` (yaklaşık 100 KB)

---

## 2️⃣ WINDOWS'A TRANSFER

### Seçenek A: USB
```
willpay_pos.zip → USB'ye kopyala
→ Windows bilgisayara tak
→ C:\ dizinine çıkar
```

### Seçenek B: Cloud
```
willpay_pos.zip → Google Drive/OneDrive/Dropbox
→ Windows'ta indir
→ C:\ dizinine çıkar
```

### Seçenek C: Email
```
willpay_pos.zip → Email ile kendinize gönderin
→ Windows'ta indir
→ C:\ dizinine çıkar
```

---

## 3️⃣ WINDOWS'TA KURULUM

### Klasör yapısı:
```
C:\willpay_pos\
├── pos_monitor.py          ⭐ Ana program
├── requirements.txt        📦 Bağımlılıklar
├── start_monitor.bat       🚀 Başlatma
├── build_exe.bat           📦 .exe oluşturma
└── *.md                    📚 Dokümantasyon
```

### Python Kur (Windows):
```
1. https://python.org/downloads
2. Python 3.10 veya üzeri indir
3. Kur → ✅ "Add Python to PATH" işaretle!
4. Kontrol: cmd → python --version
```

### Bağımlılıkları Yükle:
```cmd
cd C:\willpay_pos
pip install -r requirements.txt
```

---

## 4️⃣ ODOO KURULUM (Windows)

### Adım 1: İndir
```
https://www.odoo.com/page/download
→ Community Edition (ücretsiz)
→ Windows installer (.exe)
```

### Adım 2: Kur
```
1. odoo_xxx.exe dosyasını çalıştır
2. Next, Next, Install
3. 10 dakika bekle (PostgreSQL de kurulur)
```

### Adım 3: Başlat
```
1. Browser otomatik açılır: http://localhost:8069
2. Database oluştur (demo data ile)
3. "Point of Sale" modülünü aktif et
4. POS ekranını aç
```

### Adım 4: Ürün Ekle
```
1. Odoo → Inventory → Products
2. Yeni ürün oluştur:
   - Waffle (35₺)
   - Kahve (15₺)
3. "Available in POS" işaretle
```

---

## 5️⃣ POS MONITOR BAŞLAT

### Basit Test:
```cmd
cd C:\willpay_pos
python pos_monitor.py
```

**Log'da göreceksiniz (2 saniye sonra):**
```
🚀 Otomatik başlatma aktif...
🔍 POS aranıyor...
✅ POS bulundu: Odoo
✅ Otomatik bağlanıldı!
▶️ İzleme başlatıldı!
```

---

## 6️⃣ TEST

### Odoo POS'ta:
```
1. Ürün ekle (Waffle)
2. Ürün ekle (Kahve)
3. "Validate" (Ödeme) butonuna bas
```

### POS Monitor'de:
```
🔔 DEĞİŞİKLİK! 0₺ → 35₺
🔔 DEĞİŞİKLİK! 35₺ → 50₺
💳 ÖDEME TAMAMLANDI!
📤 Backend'e gönderiliyor...
✅ QR gösterildi! 🎉
```

---

## 🚀 OTOMATİK BAŞLATMA (Opsiyonel)

### Startup Klasörüne Ekle:

```cmd
1. start_monitor.bat → Sağ tık → Kısayol oluştur
2. Windows + R → shell:startup → Enter
3. Kısayolu yapıştır
```

**Windows her açıldığında otomatik başlar!**

---

## 📦 .EXE OLUŞTUR (Opsiyonel)

### Python'suz Çalışan Versiyon:

```cmd
cd C:\willpay_pos
build_exe.bat
```

**Sonuç:**
```
dist\WillPayPOSMonitor.exe
```

**Artık bu .exe:**
- Python gerektirmez
- Çift tıkla çalışır
- Başka bilgisayarlara kopyalanabilir

---

## ✅ KONTROL LİSTESİ

**macOS'ta (ŞİMDİ):**
- [ ] venv ve cache temizlendi
- [ ] willpay_pos.zip oluşturuldu
- [ ] Windows'a transfer edildi

**Windows'ta:**
- [ ] Zip çıkarıldı (C:\willpay_pos\)
- [ ] Python kuruldu
- [ ] pip install -r requirements.txt
- [ ] Odoo kuruldu
- [ ] Odoo POS açık
- [ ] pos_monitor.py çalıştırıldı
- [ ] Otomatik bağlandı
- [ ] Test başarılı
- [ ] QR açıldı! 🎉

---

## 🎯 ŞİMDİ YAPACAKLARINIZ (macOS)

### 1. Temizlik:
```bash
cd '/Users/onurtezel/granny'"'"'s_waffle_QR'
rm -rf venv __pycache__ *.pyc test_qr.png
```

### 2. Zip'le:
```bash
cd ..
zip -r willpay_pos.zip 'granny'"'"'s_waffle_QR'
```

### 3. Transfer Et:
```
willpay_pos.zip → USB/Cloud/Email → Windows
```

---

## 📋 WINDOWS'TA YAPACAKLARINIZ

```
1. Zip'i C:\ dizinine çıkar
2. Python kur (python.org)
3. pip install -r requirements.txt
4. Odoo kur ve POS aç
5. python pos_monitor.py
6. TEST ET!
```

---

## 🎉 BAŞARI SONRASI

**.exe oluştur (opsiyonel):**
```cmd
build_exe.bat
→ WillPayPOSMonitor.exe oluşur
→ Startup'a at
→ UNUTUN!
```

---

**macOS'ta dosyaları zip'leyin, ben komutları hazırladım!** 🚀

Zip'ledikten sonra söyleyin! 😊

