@echo off
echo ========================================
echo   WillPay POS Monitor - EXE Olusturma
echo ========================================
echo.

REM PyInstaller yukle
echo PyInstaller kontrol ediliyor...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller yukleniyor...
    pip install pyinstaller
    echo.
)

REM Eski build temizle
echo Eski build dosyalari temizleniyor...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del *.spec 2>nul
echo Temizlendi!
echo.

REM EXE olustur
echo ========================================
echo   EXE Olusturuluyor...
echo ========================================
echo.
echo [1/3] Bagimliliklari analiz ediliyor...
echo [2/3] Dosyalar derleniyor...
echo [3/3] EXE paketi hazirlaniyor...
echo.

pyinstaller ^
    --onefile ^
    --noconsole ^
    --name="WillPayPOSMonitor" ^
    --add-data="*.png;." ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=qrcode ^
    --hidden-import=requests ^
    --hidden-import=PIL ^
    pos_monitor.py

echo.
echo ========================================
if exist dist\WillPayPOSMonitor.exe (
    echo   BASARILI!
    echo ========================================
    echo.
    echo [OK] EXE dosyasi olusturuldu!
    echo.
    echo Konum: dist\WillPayPOSMonitor.exe
    echo.
    
    REM Dosya boyutu
    for %%A in (dist\WillPayPOSMonitor.exe) do (
        set size=%%~zA
    )
    echo Boyut: %size% bytes
    echo.
    echo ========================================
    echo   KULLANIM
    echo ========================================
    echo.
    echo Test:
    echo   dist\WillPayPOSMonitor.exe
    echo.
    echo Otomatik Baslatma:
    echo   1. dist\WillPayPOSMonitor.exe -> Kisayol olustur
    echo   2. Windows + R -> shell:startup
    echo   3. Kisayolu yapiştir
    echo.
    echo Dagitim:
    echo   dist\WillPayPOSMonitor.exe -> Diger bilgisayarlara kopyala
    echo.
    
) else (
    echo   HATA!
    echo ========================================
    echo.
    echo [!] EXE olusturulamadi!
    echo.
    echo Hata log: build\WillPayPOSMonitor\warn-WillPayPOSMonitor.txt
    echo.
)

echo.
pause

