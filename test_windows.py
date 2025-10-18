"""
Windows Test Script - pywinauto kontrolü
"""
import sys

print("=" * 60)
print("🪟 Windows UI Automation Test")
print("=" * 60)
print()

# 1. pywinauto kontrolü
print("1️⃣ pywinauto yüklü mü?")
try:
    import pywinauto
    print(f"   ✅ Yüklü - Version: {pywinauto.__version__}")
except ImportError:
    print("   ❌ Yüklü değil!")
    print("   📦 Yüklemek için: pip install pywinauto")
    sys.exit(1)

print()

# 2. Açık pencereleri listele
print("2️⃣ Açık pencereler:")
try:
    from pywinauto import Desktop
    
    desktop = Desktop(backend="uia")
    windows = desktop.windows()
    
    print(f"   📊 Toplam {len(windows)} pencere bulundu:")
    print()
    
    for i, window in enumerate(windows[:10], 1):
        try:
            title = window.window_text()
            if title and len(title) > 2:
                print(f"   {i:2d}. {title}")
        except:
            pass
            
except Exception as e:
    print(f"   ❌ Hata: {str(e)}")

print()

# 3. POS programı var mı?
print("3️⃣ POS programı algılandı mı?")
pos_keywords = ['POS', 'Restaurant', 'Loyverse', 'Square', 'Toast', 'Kasa']

found_pos = False
for window in windows:
    try:
        title = window.window_text()
        if any(kw.lower() in title.lower() for kw in pos_keywords):
            print(f"   ✅ POS BULUNDU: {title}")
            found_pos = True
    except:
        pass

if not found_pos:
    print("   ❌ POS programı bulunamadı")
    print("   💡 Loyverse veya başka bir POS programı açın")

print()

# 4. Notepad testi
print("4️⃣ Notepad testi (basit test):")
print("   📝 Notepad açın ve içine 'Toplam: 90₺' yazın")
print("   Sonra bu scripti tekrar çalıştırın")
print()

try:
    notepad = desktop.window(title_re=".*Notepad.*")
    if notepad.exists():
        print("   ✅ Notepad bulundu!")
        
        # Notepad'deki metni oku
        edit_control = notepad.child_window(class_name="Edit")
        text = edit_control.window_text()
        
        if text:
            print(f"   📄 Notepad içeriği: {text[:100]}")
            
            # Toplam ara
            if 'toplam' in text.lower():
                print("   ✅ 'Toplam' kelimesi bulundu!")
                print("   💡 POS Monitor benzer şekilde çalışacak")
        else:
            print("   ℹ️  Notepad boş")
    else:
        print("   ℹ️  Notepad açık değil")
        
except:
    print("   ℹ️  Notepad bulunamadı")

print()
print("=" * 60)
print("✅ Test tamamlandı!")
print()
print("Sonraki adım:")
print("  1. Loyverse POS indir: https://loyverse.com/download")
print("  2. python pos_monitor.py çalıştır")
print("  3. Test et!")
print("=" * 60)

