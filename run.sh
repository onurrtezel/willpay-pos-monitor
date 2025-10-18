#!/bin/bash
# Quick Run Script - Tüm programları kolayca çalıştırın

VENV_PYTHON="/Users/onurtezel/granny's_waffle_QR/venv/bin/python"

case "$1" in
    "pos")
        echo "🧇 POS UI başlatılıyor..."
        $VENV_PYTHON pos_ui.py
        ;;
    "monitor")
        echo "🔍 POS Monitor başlatılıyor..."
        $VENV_PYTHON pos_monitor.py
        ;;
    "web-monitor")
        echo "🌐 Web Monitor başlatılıyor..."
        $VENV_PYTHON pos_monitor_web.py
        ;;
    "test-html")
        echo "🧪 HTML Test POS başlatılıyor..."
        open test_pos.html
        sleep 2
        $VENV_PYTHON test_html_pos.py
        ;;
    "test-api")
        echo "🧪 API Test başlatılıyor..."
        $VENV_PYTHON test_api.py
        ;;
    "test-win")
        echo "🪟 Windows Test başlatılıyor..."
        $VENV_PYTHON test_windows.py
        ;;
    *)
        echo "📋 WillPay POS - Kullanım:"
        echo ""
        echo "  ./run.sh pos          - POS UI başlat"
        echo "  ./run.sh monitor      - POS Monitor başlat"
        echo "  ./run.sh web-monitor  - Web Monitor başlat"
        echo "  ./run.sh test-html    - HTML test başlat"
        echo "  ./run.sh test-api     - API test"
        echo "  ./run.sh test-win     - Windows test"
        echo ""
        ;;
esac

