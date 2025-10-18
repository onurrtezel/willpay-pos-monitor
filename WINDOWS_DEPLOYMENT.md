# 🪟 Windows Bilgisayarda Deployment

## 📋 Sistem Özeti

✅ **Hazır Olan:**
1. ✅ POS UI (PyQt6) - Ödeme sistemi
2. ✅ QR kod üretimi - `/receipt/new` formatında
3. ✅ Backend entegrasyonu - WillPay API
4. ✅ UI Automation desteği - AutomationId'ler
5. ✅ Çift ödeme koruması
6. ✅ Mobil QR handler kodu

---

## 🖥️ Windows Bilgisayarda Kurulum

### 1. Dosyaları Windows'a Taşıyın

Tüm proje dosyalarını Windows bilgisayara kopyalayın:
```
C:\willpay_pos\
├── pos_ui.py
├── requirements.txt
├── test_api.py
├── ui_automation_test.py
├── README.md
└── ...
```

---

### 2. Python Kurulumu (Windows)

#### Python İndirin:
```
https://www.python.org/downloads/
Python 3.10 veya üzeri
```

**Önemli:** Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin!

#### Kontrol Edin:
```cmd
python --version
pip --version
```

---

### 3. Bağımlılıkları Yükleyin

```cmd
cd C:\willpay_pos
pip install -r requirements.txt
```

**Veya tek tek:**
```cmd
pip install PyQt6 qrcode Pillow requests pywinauto
```

---

### 4. Backend URL'ini Ayarlayın

`pos_ui.py` dosyasını açın ve backend adresini güncelleyin:

```python
# Satır 40-42 civarı
BACKEND_URL = "http://192.168.1.103:8000"  # Şu anki
# Veya
BACKEND_URL = "http://localhost:8000"      # Eğer backend aynı makinede
```

---

### 5. POS'u Başlatın

```cmd
python pos_ui.py
```

**Pencere açılacak:**
- Sol taraf: Ürünler (Waffle, Smoothie, Kahve)
- Sağ taraf: Sepet ve ödeme butonu

---

## 🤖 UI Automation Kullanımı

UI Automation, **başka bir uygulamanın** POS'tan fiş verilerini otomatik okumasını sağlar.

### Ne İçin Kullanılır?

1. **Otomatik Fiş Okuma:** Başka bir program POS'taki sepeti okuyabilir
2. **Entegrasyon:** Muhasebe/ERP sistemleriyle otomatik veri aktarımı
3. **Test Otomasyonu:** POS'u otomatik test etme
4. **Raporlama:** Satış verilerini otomatik toplama

### Örnek Kullanım:

```python
# ui_automation_test.py çalıştırın
python ui_automation_test.py
```

**Ne Yapar?**
- POS penceresine bağlanır
- Sepetteki ürünleri okur (`receipt_item_0_name`, `receipt_item_0_price`, vs.)
- Toplam tutarı okur (`TotalLabel`)
- Ödeme butonuna basabilir (`PayButton`)

### AutomationId Listesi:

| Element | AutomationId | Açıklama |
|---------|--------------|----------|
| Toplam Tutar | `TotalLabel` | Sepet toplamı |
| Ödeme Butonu | `PayButton` | Ödeme tamamla |
| Ürün Adı | `receipt_item_0_name` | İlk ürünün adı |
| Ürün Fiyatı | `receipt_item_0_price` | İlk ürünün fiyatı |
| Ürün Miktarı | `receipt_item_0_quantity` | İlk ürünün miktarı |

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Manuel POS Kullanımı (Basit)

```
1. POS'u aç: python pos_ui.py
2. Ürün ekle: Sol taraftan tıkla
3. Ödeme yap: "Ödeme Tamamla" butonuna bas
4. QR göster: Popup açılır, müşteri tarar
5. Fiş düşer: Backend'e ve mobil app'e
```

**Bu senaryoda UI Automation'a GEREK YOK!**

---

### Senaryo 2: Başka Program ile Entegrasyon (UI Automation)

Örnek: Muhasebe programınız POS'tan veri çekmek istiyor.

```python
# muhasebe_entegrasyon.py (örnek)
from pywinauto import Application, Desktop

# POS'a bağlan
desktop = Desktop(backend="uia")
pos_window = desktop.window(title_re=".*Granny's Waffle.*")

# Toplam tutarı oku
total_label = pos_window.child_window(auto_id="TotalLabel", control_type="Text")
total_amount = total_label.window_text()  # "Toplam: 90₺"

# İlk ürünü oku
item_name = pos_window.child_window(auto_id="receipt_item_0_name").window_text()
item_price = pos_window.child_window(auto_id="receipt_item_0_price").window_text()

# Muhasebe sistemine aktar
send_to_accounting_system({
    "total": total_amount,
    "items": [{"name": item_name, "price": item_price}]
})
```

---

### Senaryo 3: Otomatik Test (UI Automation)

```cmd
python ui_automation_test.py
```

**Test Sonucu:**
```
✅ TotalLabel erişilebilir
✅ PayButton erişilebilir
✅ Cart Items erişilebilir
```

---

## 📝 Hangi Senaryoyu Kullanmalısınız?

### 🟢 Senaryo 1 (Manuel) - Çoğu Durumda Yeterli
- ✅ Kasiyerler manuel kullanıyor
- ✅ QR kod müşteriye gösteriliyor
- ✅ Backend'e otomatik kaydediliyor
- ❌ UI Automation'a gerek YOK

### 🟡 Senaryo 2 (Entegrasyon) - Özel Durumlar
- ✅ Başka bir program POS'tan veri almalı
- ✅ ERP/Muhasebe entegrasyonu
- ✅ Otomatik raporlama
- ✅ UI Automation GEREKLI

### 🟠 Senaryo 3 (Test) - Geliştirme/QA
- ✅ Otomatik test senaryoları
- ✅ Kalite kontrolü
- ✅ UI Automation GEREKLI

---

## 🚀 Windows'ta Başlatma

### Basit Başlatma:
```cmd
cd C:\willpay_pos
python pos_ui.py
```

### Windows Servis Olarak (Opsiyonel):

#### 1. Kısayol Oluşturun:
- `pos_ui.py` üzerine sağ tık
- "Create shortcut"
- Kısayolu `Startup` klasörüne taşıyın:
  ```
  C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
  ```

#### 2. Batch Script (.bat):
```batch
@echo off
cd C:\willpay_pos
python pos_ui.py
```
Kaydedin: `start_pos.bat`

---

## 🔧 Sorun Giderme

### POS Açılmıyor:
```cmd
# Python yüklü mü?
python --version

# PyQt6 yüklü mü?
python -c "import PyQt6; print('OK')"

# Hata mesajı nedir?
python pos_ui.py
```

### Backend'e Bağlanamıyor:
```cmd
# Backend çalışıyor mu?
curl http://192.168.1.103:8000/health

# Veya tarayıcıda:
http://192.168.1.103:8000/health
```

### UI Automation Çalışmıyor:
```cmd
# pywinauto yüklü mü?
pip install pywinauto

# POS açık mı?
python ui_automation_test.py
```

---

## 📊 Proje Yapısı

```
C:\willpay_pos\
│
├── pos_ui.py                    ⭐ ANA UYGULAMA
├── requirements.txt             📦 Bağımlılıklar
│
├── test_api.py                  🧪 Backend test
├── ui_automation_test.py        🤖 UI Automation test
│
├── README.md                    📚 Genel dokümantasyon
├── INTEGRATION.md               🔌 Backend entegrasyon
├── QUICKSTART.md                🚀 Hızlı başlangıç
├── MOBILE_SIMPLE_HANDLER.md     📱 Mobil QR handler
└── WINDOWS_DEPLOYMENT.md        🪟 Bu dosya
```

---

## ✅ Kontrol Listesi

**POS Kullanımı İçin:**
- [ ] Python yüklü (3.10+)
- [ ] Bağımlılıklar yüklü (`pip install -r requirements.txt`)
- [ ] Backend çalışıyor (http://192.168.1.103:8000/health)
- [ ] `python pos_ui.py` çalıştırıldı
- [ ] Pencere açıldı ve ürünler görünüyor

**UI Automation İçin (Opsiyonel):**
- [ ] pywinauto yüklü
- [ ] POS açık ve çalışıyor
- [ ] `python ui_automation_test.py` testi geçti

---

## 🎯 ÖNERİ

### Çoğu Kullanıcı İçin:
```cmd
# 1. Kurulum
pip install PyQt6 qrcode Pillow requests

# 2. Başlat
python pos_ui.py

# 3. Kullan
# Sol taraftan ürün seç → Ödeme yap → QR göster
```

**UI Automation'a gerek YOK!** Sadece POS'u kullanın.

### İleri Seviye (ERP Entegrasyonu):
```cmd
# UI Automation test et
python ui_automation_test.py

# Kendi entegrasyon scriptinizi yazın
# (Örnek: muhasebe_entegrasyon.py)
```

---

## 🎉 Özet

**Yapmanız Gereken:**
1. ✅ Dosyaları Windows'a kopyala
2. ✅ Python kur
3. ✅ `pip install -r requirements.txt`
4. ✅ `python pos_ui.py`
5. ✅ Kullanmaya başla!

**UI Automation:**
- Sadece **başka programlarla entegrasyon** gerekiyorsa kullanın
- Manuel kullanım için **GEREK YOK**

**Backend'i düzeltin, sonra POS hazır kullanıma!** 🚀


