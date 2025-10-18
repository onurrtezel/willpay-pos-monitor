@echo off
REM Granny's Waffle POS - Baslatma Script

echo ========================================
echo   Granny's Waffle POS Baslatiliyor
echo ========================================
echo.

cd /d "C:\granny's_waffle_QR"

REM Backend kontrol
echo Backend kontrolu...
curl -s http://192.168.1.103:8000/health >nul 2>&1
if errorlevel 1 (
    echo [UYARI] Backend calismiyor!
    echo Backend'i baslatmayi unutmayin.
    echo.
) else (
    echo [OK] Backend calisiyor!
    echo.
)

REM POS UI'yi basla
echo POS UI baslatiliyor...
echo.
python pos_ui.py

REM Hata durumunda
if errorlevel 1 (
    echo.
    echo [HATA] POS UI baslamadi!
    echo Python veya PyQt6 kontrol edin:
    echo   pip install PyQt6 qrcode Pillow requests
    pause
)

