# 🧇 WillPay POS Monitor

**UI Automation ile POS sistemlerinden veri çeker, WillPay backend'e gönderir, QR kod oluşturur.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Özellikler

- ✅ **Kendi POS Sistemi** (`pos_ui.py`) - Tam fonksiyonel restaurant POS
- ✅ **UI Automation** (`pos_monitor.py`) - Mevcut POS programlarından veri çekme
- ✅ **Backend Entegrasyonu** - WillPay API ile çalışır
- ✅ **QR Kod Otomatik** - Ödeme sonrası QR popup
- ✅ **Tamamen Otomatik** - POS bulma, bağlanma, izleme
- ✅ **Windows Desteği** - Startup, .exe, servis

---

## 🚀 Hızlı Başlangıç

### Basit Kullanım (Kendi POS):

```bash
# Kurulum
pip install PyQt6 qrcode Pillow requests

# Başlat
python pos_ui.py
```

### Gelişmiş Kullanım (Mevcut POS İzleme):

```bash
# Kurulum (Windows)
pip install pywinauto

# Başlat
python pos_monitor.py
```

---

## 📦 Kurulum

### Windows:

```cmd
git clone https://github.com/onurtezel/willpay-pos-monitor.git
cd willpay-pos-monitor
pip install -r requirements.txt
```

### Basit Kullanım:
```cmd
python pos_ui.py
```

### Gelişmiş Kullanım:
```cmd
python pos_monitor.py
```

---

## 🎯 İki Kullanım Modu

### 1. Kendi POS Sistemimiz (`pos_ui.py`)

Tam fonksiyonel restaurant POS:
- Sol panel: Ürün kategorileri (Waffle, Smoothie, Kahve)
- Sağ panel: Sepet, toplam tutar, ödeme
- Backend entegrasyonu
- QR kod otomatik açılır

**Kullanım:**
```cmd
python pos_ui.py
```

**Avantaj:** Basit, hızlı, başka programa gerek yok!

---

### 2. Mevcut POS İzleyici (`pos_monitor.py`)

Loyverse, Odoo, TouchBistro gibi programlardan UI Automation ile veri çeker:

**Desteklenen Programlar:**
- Loyverse POS
- Odoo POS
- Square POS
- TouchBistro
- ve diğerleri...

**Özellikler:**
- Otomatik POS algılama
- Gerçek zamanlı değişiklik tespiti (0.5s)
- Ödeme anında otomatik QR
- Arka plan çalışma

**Kullanım:**
```cmd
python pos_monitor.py
```

---

## 🖥️ Ekran Görüntüleri

### POS UI (pos_ui.py):
```
┌─────────────────────────────────────────────┐
│  🧇 Granny's Waffle - POS System           │
├──────────────────┬──────────────────────────┤
│  📂 Waffle      │  🛒 Sepet                │
│  🍫 Çikolatalı  │  Çikolatalı Waffle 35₺  │
│  🍌 Muzlu       │  Türk Kahvesi 15₺       │
│                  │  ────────────────────    │
│  📂 Smoothie    │  Toplam: 50₺            │
│  🥤 Karışık     │  [💳 Ödeme Tamamla]     │
└──────────────────┴──────────────────────────┘
```

### POS Monitor (pos_monitor.py):
```
[12:30:02] ✅ POS bulundu: Loyverse
[12:30:03] ▶️ İzleme başlatıldı (0.5s)
[12:35:15] 🔔 DEĞİŞİKLİK! 0₺ → 35₺
[12:36:00] 💳 ÖDEME TAMAMLANDI!
[12:36:01] ✅ QR gösterildi!
```

---

## 📚 Dokümantasyon

- **OKUBENI.txt** - İlk okuyun!
- **BASIT_KULLANIM.md** - En kolay yöntem
- **TAMAMEN_OTOMATIK.md** - Otomatik mod
- **OTOMATIK_BASLATMA.md** - Windows Startup
- **EXE_OLUSTURMA.md** - .exe yapma
- **ANTIVIRUS_COZUM.md** - Virüs uyarısı çözümü

[Tüm Dokümantasyon](/)

---

## 🔧 Yapılandırma

### Backend URL:

```python
# pos_ui.py ve pos_monitor.py
BACKEND_URL = "http://192.168.1.103:8000"
```

### Otomatik Başlatma:

```cmd
start_pos.bat → Kısayol → shell:startup
```

---

## 🧪 Test

### Backend Testi:
```bash
python test_api.py
```

### Windows UI Automation Testi:
```bash
python test_windows.py
```

---

## 📦 .EXE Oluşturma

```cmd
build_exe.bat
```

Sonuç: `dist\WillPayPOSMonitor.exe`

---

## 🎯 Sistem Gereksinimleri

- **İşletim Sistemi:** Windows 10/11 (UI Automation için)
- **Python:** 3.10 veya üzeri
- **Backend:** WillPay API (http://192.168.1.103:8000)

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

---

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 👤 Geliştirici

**Onur Tezel**

WillPay için geliştirildi - 2025

---

## ⭐ Beğendiyseniz Yıldız Verin!

GitHub'da ⭐ vermeyi unutmayın!

---

## 🔗 Linkler

- [WillPay Backend](http://192.168.1.103:8000)
- [Dokümantasyon](/)
- [Issues](https://github.com/onurtezel/willpay-pos-monitor/issues)

---

Made with ❤️ for WillPay
