#!/bin/bash
# Quick Demo Script for WillPay POS Integration

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🧇 Granny's Waffle - WillPay POS Demo               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check backend
echo -e "${BLUE}🔍 Checking WillPay Backend...${NC}"
if curl -s http://192.168.1.103:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running!${NC}"
    curl -s http://192.168.1.103:8000/health | python3 -m json.tool
else
    echo -e "${YELLOW}⚠️  Backend not reachable at http://192.168.1.103:8000${NC}"
    echo "   Please make sure the backend is running."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Quick test
echo -e "${BLUE}🧪 Running Quick Test...${NC}"
python3 test_api.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Instructions
echo -e "${YELLOW}🚀 Ready to start POS system!${NC}"
echo ""
echo "To launch POS UI:"
echo "   python3 pos_ui.py"
echo ""
echo "To create sample receipts:"
echo "   python3 test_api.py --samples"
echo ""
echo "To test UI Automation (Windows only):"
echo "   python3 ui_automation_test.py"
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║  📚 Documentation                                     ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║  • README.md         - Main documentation             ║"
echo "║  • INTEGRATION.md    - Backend integration details    ║"
echo "║  • QUICKSTART.md     - Quick start guide              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

