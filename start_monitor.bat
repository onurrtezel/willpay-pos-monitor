@echo off
REM WillPay POS Monitor - Otomatik Başlatma Script
REM Bu script bilgisayar açılınca otomatik çalışacak

echo ========================================
echo   WillPay POS Monitor Baslatiiliyor
echo ========================================
echo.

REM POS Monitor dizinine git
cd /d C:\willpay_pos

REM 5 saniye bekle (Windows tam açılsın)
echo Bekleniyor... (5 saniye)
timeout /t 5 /nobreak >nul

REM Backend kontrolu
echo Backend kontrolu yapiliyor...
curl -s http://192.168.1.103:8000/health >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Backend calismiyor!
    echo Backend'i baslatmayi unutmayin.
    echo.
) else (
    echo [OK] Backend calisiyor!
    echo.
)

REM Loyverse kontrol
echo Loyverse kontrolu yapiliyor...
tasklist /FI "IMAGENAME eq Loyverse.exe" 2>NUL | find /I /N "Loyverse.exe">NUL
if errorlevel 1 (
    echo [UYARI] Loyverse calismiyor!
    echo Loyverse'u manuel baslatmaniz gerekebilir.
    echo.
) else (
    echo [OK] Loyverse calisiyor!
    echo.
)

REM POS Monitor'u basla (OTOMATIK MOD)
echo.
echo ========================================
echo   POS Monitor Basladi (OTOMATIK MOD)
echo ========================================
echo.
echo [i] Program acilinca OTOMATIK olarak:
echo     1. POS'a baglanacak
echo     2. Izlemeyi baslayacak
echo     3. Odeme olunca QR gosterecek
echo.
echo [!] Hic bir sey yapmaniza gerek yok!
echo.
echo Programi kapatmak icin pencereyi kapatin.
echo ========================================
echo.

start "WillPay POS Monitor" python pos_monitor.py

REM Hata durumunda
if errorlevel 1 (
    echo.
    echo [HATA] POS Monitor baslamadi!
    echo Python veya bagimliliklari kontrol edin.
    pause
)

