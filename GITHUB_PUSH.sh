#!/bin/bash
# GitHub'a Otomatik Yükleme Scripti

echo "🚀 GitHub'a Yükleme Başlıyor..."
echo ""

# GitHub kullanıcı adını sor
read -p "GitHub kullanıcı adınız (örn: onurtezel): " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Kullanıcı adı boş olamaz!"
    exit 1
fi

echo ""
echo "📝 Repo bilgileri:"
echo "   Kullanıcı: $GITHUB_USER"
echo "   Repo adı: willpay-pos-monitor"
echo "   URL: https://github.com/$GITHUB_USER/willpay-pos-monitor"
echo ""

read -p "Devam edilsin mi? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ İptal edildi"
    exit 0
fi

cd '/Users/onurtezel/granny'"'"'s_waffle_QR'

# Remote ekle
echo ""
echo "🔗 Remote ekleniyor..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$GITHUB_USER/willpay-pos-monitor.git"
echo "✅ Remote eklendi"

# Branch kontrol
echo ""
echo "🌿 Branch kontrol ediliyor..."
git branch -M main
echo "✅ Main branch hazır"

# Push
echo ""
echo "📤 GitHub'a yükleniyor..."
echo "⚠️  GitHub kullanıcı adı ve Personal Access Token gireceksiniz"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════"
    echo "✅ BAŞARILI!"
    echo "═══════════════════════════════════════"
    echo ""
    echo "🔗 Repo linki:"
    echo "   https://github.com/$GITHUB_USER/willpay-pos-monitor"
    echo ""
    echo "🌐 Clone komutu:"
    echo "   git clone https://github.com/$GITHUB_USER/willpay-pos-monitor.git"
    echo ""
else
    echo ""
    echo "❌ Push başarısız!"
    echo ""
    echo "💡 GitHub'da repo oluşturdunuz mu?"
    echo "   https://github.com/new"
    echo ""
    echo "💡 Personal Access Token var mı?"
    echo "   Settings → Developer settings → Tokens"
    echo ""
fi

