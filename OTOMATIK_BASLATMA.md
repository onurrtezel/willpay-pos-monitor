# 🚀 Windows'ta Otomatik Başlatma

## 🎯 3 Yöntem

---

## 1️⃣ STARTUP KLASÖRÜ (EN KOLAY) ⭐

### Adım 1: Kısayol Oluştur

1. **`start_monitor.bat`** dosyasına sağ tıklayın
2. **"Kısayol oluştur"** seçin
3. Kısayolu kesin (Ctrl+X)

### Adım 2: Startup Klasörüne Yapıştır

```
Windows tuşu + R → shell:startup → Enter
```

Açılan klasöre kısayolu yapıştırın:
```
C:\Users\<KullaniciAdi>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

### ✅ Bitti!

**Bilgisayar her açıldığında:**
- 5 saniye bekler
- Backend kontrolü yapar
- Loyverse kontrolü yapar
- POS Monitor'ü başlatır

---

## 2️⃣ TASK SCHEDULER (DAHA PROFESYONEL) ⭐⭐

### Adım 1: Task Scheduler Aç

```
Windows tuşu → "Task Scheduler" yazın → Aç
```

### Adım 2: Yeni Task Oluştur

1. **Sağ panelde:** "Create Basic Task"
2. **Name:** "WillPay POS Monitor"
3. **Trigger:** "When the computer starts"
4. **Action:** "Start a program"
5. **Program:** 
   ```
   C:\willpay_pos\start_monitor.bat
   ```
6. **Start in:** 
   ```
   C:\willpay_pos
   ```

### Adım 3: Gecikmeli Başlatma (Önemli!)

1. Task'a çift tıklayın
2. **"Triggers"** tab → "Edit"
3. **"Delay task for:"** → **30 seconds** ← Windows tam açılsın
4. **OK**

### Adım 4: Yüksek Öncelik (Opsiyonel)

1. **"General"** tab
2. **"Run with highest privileges"** ← İşaretle
3. **OK**

### ✅ Bitti!

**Artık bilgisayar her açıldığında:**
- 30 saniye bekler
- Otomatik başlar

---

## 3️⃣ WINDOWS SERVIS (GELİŞMİŞ) ⭐⭐⭐

### NSSM (Non-Sucking Service Manager) ile

#### İndirme:
```
https://nssm.cc/download
```

#### Kurulum:

```cmd
REM NSSM'i C:\nssm klasörüne çıkarın

REM Admin CMD açın
cd C:\nssm\win64

REM Servis oluştur
nssm install WillPayPOSMonitor "C:\Python310\python.exe" "C:\willpay_pos\pos_monitor.py"

REM Startup type ayarla
nssm set WillPayPOSMonitor Start SERVICE_AUTO_START

REM Servis başlat
nssm start WillPayPOSMonitor
```

#### Servis Yönetimi:

```cmd
REM Servis durumu
nssm status WillPayPOSMonitor

REM Servis durdur
nssm stop WillPayPOSMonitor

REM Servis sil
nssm remove WillPayPOSMonitor confirm
```

---

## 📊 Karşılaştırma

| Yöntem | Kolay | Güvenilir | Otomatik Restart |
|--------|-------|-----------|------------------|
| **Startup Klasörü** | ⭐⭐⭐ | ⭐⭐ | ❌ |
| **Task Scheduler** | ⭐⭐ | ⭐⭐⭐ | ⚠️ Ayarlanabilir |
| **Windows Servis** | ⭐ | ⭐⭐⭐ | ✅ Otomatik |

---

## 🎯 ÖNERİM

### Ev/Küçük İşletme:
→ **Startup Klasörü** (En kolay)

### Profesyonel:
→ **Task Scheduler** (Daha kontrol)

### Enterprise:
→ **Windows Servis** (7/24 çalışma)

---

## 🔧 GELİŞMİŞ: Crash Durumunda Yeniden Başlatma

### start_monitor.bat'ı güncelleyin:

```batch
@echo off
:RESTART
echo POS Monitor baslatiliyor...
python pos_monitor.py

REM Crash durumunda yeniden başlat
echo.
echo [UYARI] Program kapandi! 10 saniye sonra yeniden baslatiliyor...
timeout /t 10
goto RESTART
```

**Bu script:** Program crash olsa bile 10 saniye sonra yeniden başlatır.

---

## 📋 KONTROL LİSTESİ

**Otomatik Başlatma İçin:**

- [ ] `start_monitor.bat` dosyası hazır
- [ ] Dosya yolu doğru: `C:\willpay_pos\`
- [ ] Python PATH'de var
- [ ] Startup klasörüne kısayol eklendi
- [ ] Bilgisayar yeniden başlatıldı (test için)
- [ ] POS Monitor otomatik açıldı mı?

---

## 🧪 TEST

### Otomatik Başlatmayı Test Edin:

1. Startup klasörüne kısayol ekleyin
2. Bilgisayarı **yeniden başlatın**
3. 30 saniye bekleyin
4. **POS Monitor penceresi açılmalı**

---

## ✅ SONUÇ

**Artık:**
```
Windows açılır
    ↓ 5-30 saniye bekler
POS Monitor otomatik başlar
    ↓ Loyverse'e bağlanır
İzlemeye başlar
    ↓ Ödeme olunca
QR otomatik açılır
```

**Hiç dokunmanıza gerek yok!** 🎉

---

## 💡 BİR ADIM DAHA

Loyverse'ü de otomatik başlatmak isterseniz:

`start_monitor.bat` dosyasına ekleyin:

```batch
REM Loyverse'u başlat (eğer kurulu değilse)
start "" "C:\Program Files\Loyverse\Loyverse.exe"
timeout /t 10

REM Sonra POS Monitor başlat
python pos_monitor.py
```

---

**Startup klasörüne kısayol atın, test edin!** 🚀

