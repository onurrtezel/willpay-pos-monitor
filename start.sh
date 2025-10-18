#!/bin/bash
# Quick Start Script for WillPay POS System

echo "🧇 Granny's Waffle - WillPay POS System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Requirements installed"
echo ""

# Start backend in background
echo "🚀 Starting backend server..."
python backend.py &
BACKEND_PID=$!
echo "✅ Backend running on PID: $BACKEND_PID"
echo ""

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start POS UI
echo "🖥️  Starting POS UI..."
python pos_ui.py

# Cleanup: Kill backend when UI closes
echo ""
echo "🧹 Cleaning up..."
kill $BACKEND_PID
echo "✅ Backend stopped"
echo ""
echo "👋 Thank you for using WillPay POS!"

