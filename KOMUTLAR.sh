#!/bin/bash
echo "🚀 GitHub Push Başlatılıyor..."
echo ""
echo "⚠️  GitHub kullanıcı adı ve token gerekecek!"
echo ""

cd '/Users/onurtezel/granny'"'"'s_waffle_QR'

# Remote ekle (kullanıcı adını değiştirin!)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/onurtezel/willpay-pos-monitor.git

# Branch ayarla
git branch -M main

# Push
echo ""
echo "📤 GitHub'a yükleniyor..."
echo "Username: onurtezel"
echo "Password: Personal Access Token girin"
echo ""
git push -u origin main

echo ""
echo "✅ Başarılı!"
echo "🔗 https://github.com/onurtezel/willpay-pos-monitor"
