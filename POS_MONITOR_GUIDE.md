# 🔍 POS Monitor - Kullanım Kılavuzu

## 🎯 Ne İşe Yarar?

**Mevcut POS sisteminizden** (TouchBistro, Square, vs.) verileri **UI Automation ile** okur ve **WillPay'e** gönderir.

```
[Mevcut POS Ekranı] 
        ↓ UI Automation
[POS Monitor] (Bu program)
        ↓ Backend'e gönder
[WillPay Backend]
        ↓ QR Oluştur
[Müşteriye Göster]
```

---

## 🚀 Hızlı Başlangıç

### Windows'ta:

```cmd
cd C:\willpay_pos
python pos_monitor.py
```

Pencere açılacak:
- **🔗 POS'a Bağlan**: Mevcut POS programını bulur
- **▶️ İzlemeyi Başlat**: Otomatik veri okumaya başlar  
- **📤 Manuel Gönder**: Tek seferlik test için

---

## 📋 Adım Adım Kullanım

### 1️⃣ POS Programınızı Açın

Örnek:
- TouchBistro
- Square POS
- Clover
- Ya da herhangi bir POS programı

**Önemli:** POS programı **görünür** olmalı (minimize değil)

---

### 2️⃣ POS Monitor'ü Başlatın

```cmd
python pos_monitor.py
```

---

### 3️⃣ POS'a Bağlanın

1. **"🔗 POS'a Bağlan"** butonuna tıklayın
2. Program tüm açık pencereleri listeler:
   ```
   1. TouchBistro - Table 5
   2. Chrome - Facebook
   3. Word - Document1
   ```
3. POS penceresi otomatik bulunur
4. **✅ Bağlandı** mesajı görünür

---

### 4️⃣ İzlemeyi Başlatın

İki yöntem:

#### A) Otomatik İzleme:
1. **"▶️ İzlemeyi Başlat"** butonuna tıklayın
2. Her 3 saniyede POS ekranını tarar
3. Değişiklik algılandığında backend'e gönderir

#### B) Manuel Gönderim:
1. Müşteri ödeme yaptığında
2. **"📤 Manuel Gönder"** butonuna tıklayın
3. Anlık veri okur ve gönderir

---

### 5️⃣ QR Göster

- Backend'e gönderim başarılı olunca **QR popup** açılır
- Müşteriye gösterin
- Müşteri QR'ı tarar
- Fiş mobil uygulamaya/web'e düşer

---

## 🎨 Ekran Görünümü

```
┌─────────────────────────────────────────────┐
│  🔍 WillPay POS Monitor                    │
├─────────────────────────────────────────────┤
│  Durum: Bekleniyor...                      │
│                                             │
│  📝 İzlenecek POS Programı:                │
│  Pencere adını giriniz                     │
│                                             │
│  [🔗 POS'a Bağlan]                          │
│  [▶️ İzlemeyi Başlat] [📤 Manuel Gönder]    │
│                                             │
│  📋 Log:                                    │
│  ┌─────────────────────────────────────┐  │
│  │ [12:30:15] 🔍 POS aranıyor...      │  │
│  │ [12:30:16] ✅ Bağlanıldı!          │  │
│  │ [12:30:20] 📤 Veri gönderiliyor... │  │
│  │ [12:30:21] ✅ QR gösterildi!       │  │
│  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Özelleştirme

### POS Programınıza Göre Ayarlama

`pos_monitor.py` dosyasını açın ve `scan_pos()` fonksiyonunu düzenleyin:

```python
def scan_pos(self):
    """POS'tan veri oku"""
    
    # Örnek 1: Toplam tutarı oku
    total_element = self.pos_window.child_window(
        auto_id="TotalAmount",  # ← POS programınızdaki ID
        control_type="Text"
    )
    total = total_element.window_text()
    
    # Örnek 2: Ürünleri oku
    items = []
    for i in range(10):  # İlk 10 ürün
        try:
            item_name = self.pos_window.child_window(
                auto_id=f"Item_{i}_Name"  # ← POS programınızdaki ID
            ).window_text()
            
            item_price = self.pos_window.child_window(
                auto_id=f"Item_{i}_Price"
            ).window_text()
            
            items.append({
                "name": item_name,
                "price": float(item_price),
                "quantity": 1,
                "category": "food"
            })
        except:
            break
    
    # Backend'e gönder
    self.send_to_backend({
        "total_amount": float(total),
        "items": items,
        # ...
    })
```

---

## 🔍 POS Elementlerini Bulma

### Inspect Tool Kullanın:

```python
# inspect_pos.py
from pywinauto import Desktop

desktop = Desktop(backend="uia")
window = desktop.window(title_re=".*POS.*")  # POS penceresi

# Tüm elementleri listele
window.print_control_identifiers()

# Çıktı:
# Text - 'Total: $90.00'    auto_id='TotalLabel'
# Text - 'Waffle'           auto_id='Item_0_Name'
# Text - '$35.00'           auto_id='Item_0_Price'
```

Bu bilgileri kullanarak `scan_pos()` fonksiyonunu özelleştirin.

---

## 📊 Örnek Senaryolar

### Senaryo 1: TouchBistro

```python
def scan_pos(self):
    # TouchBistro'nun toplam tutarı
    total = self.pos_window.child_window(
        class_name="TotalAmountLabel"
    ).window_text()
    
    # Ürünleri oku (ListView'den)
    list_view = self.pos_window.child_window(
        class_name="ListView",
        control_type="List"
    )
    items = list_view.items()
```

### Senaryo 2: Square POS

```python
def scan_pos(self):
    # Square'in HTML elementi
    browser = self.pos_window.child_window(
        class_name="Chrome_WidgetWin_1"
    )
    
    # Web sayfasından veri çek
    # ...
```

### Senaryo 3: Özel POS

```python
def scan_pos(self):
    # OCR ile ekran okuma
    from PIL import ImageGrab
    import pytesseract
    
    # Ekran görüntüsü al
    img = ImageGrab.grab(self.pos_window.rectangle())
    
    # OCR ile metin çıkar
    text = pytesseract.image_to_string(img)
    
    # Parse et
    # ...
```

---

## 🛠️ Sorun Giderme

### Pencere Bulunamıyor:

```python
# Tüm pencereleri listele
from pywinauto import Desktop

desktop = Desktop(backend="uia")
for window in desktop.windows():
    print(window.window_text())
```

### Element Bulunamıyor:

```python
# Inspect tool kullan
window.print_control_identifiers()

# Veya
window.dump_tree()
```

### Backend'e Gönderilmiyor:

```cmd
# Backend çalışıyor mu?
curl http://192.168.1.103:8000/health

# Log'lara bak
# POS Monitor'deki log alanını kontrol edin
```

---

## 🎯 En İyi Uygulamalar

### 1. Test Modu:
İlk önce **"Manuel Gönder"** ile test edin.

### 2. Otomatik İzleme:
Çalıştığından emin olduktan sonra **"İzlemeyi Başlat"**.

### 3. Hata Yönetimi:
Log'ları sürekli kontrol edin.

### 4. Performans:
Tarama aralığını ayarlayın (3-5 saniye optimal).

---

## 📝 Kontrol Listesi

**Başlamadan Önce:**
- [ ] Python yüklü (3.10+)
- [ ] pywinauto yüklü (`pip install pywinauto`)
- [ ] POS programı açık
- [ ] Backend çalışıyor
- [ ] Windows bilgisayar

**Çalışma Sırasında:**
- [ ] POS Monitor açık
- [ ] "✅ Bağlandı" mesajı görünüyor
- [ ] Log'da hata yok
- [ ] QR popup açılıyor
- [ ] Backend'e veri gidiyor

---

## 🚀 İleri Seviye

### Hotkey İle Tetikleme:

```python
# Klavye kısayolu ekle (örn: F12)
from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.f12:
        self.manual_send()

listener = keyboard.Listener(on_press=on_press)
listener.start()
```

### Otomatik Fiş Algılama:

```python
def detect_new_receipt(self):
    """Yeni fiş algıla"""
    current_total = self.get_total()
    
    if current_total != self.last_total and current_total > 0:
        # Yeni fiş var!
        self.send_to_backend()
        
    self.last_total = current_total
```

---

## 📄 Özet

**POS Monitor:**
- ✅ Mevcut POS'tan veri çeker
- ✅ UI Automation kullanır
- ✅ Backend'e gönderir
- ✅ QR kod oluşturur
- ✅ Müşteriye gösterir

**Kullanım:**
```cmd
1. python pos_monitor.py
2. "🔗 POS'a Bağlan"
3. "▶️ İzlemeyi Başlat" veya "📤 Manuel Gönder"
4. QR göster → Müşteri tarar → Fiş düşer
```

**POS programınıza göre `scan_pos()` fonksiyonunu özelleştirin!** 🎯


