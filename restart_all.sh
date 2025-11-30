#!/bin/bash
# 🚀 FxFutbol (Spradar) Yeniden Başlatma Scripti
# Kullanım: sudo bash restart_all.sh
# NOT: Sadece fxfutbol.com.tr'yi yeniden başlatır, diğer sitelere dokunmaz!

echo "🔄 FxFutbol yeniden başlatılıyor..."
echo ""

# 1. Python cache temizle
echo "1️⃣ Python cache temizleniyor..."
find /var/www/spradar -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null
find /var/www/spradar -type f -name '*.pyc' -delete 2>/dev/null
echo "   ✅ Python cache temizlendi"
echo ""

# 2. Spradar service'i yeniden başlat
echo "2️⃣ Spradar service yeniden başlatılıyor..."
systemctl restart spradar.service
sleep 3
echo "   ✅ Spradar service yeniden başlatıldı"
echo ""

# 3. Durum kontrolü
echo "3️⃣ Servis durumu kontrol ediliyor..."
echo ""
echo -n "   📊 Spradar Service: "
systemctl is-active spradar.service && echo "✅ Çalışıyor" || echo "❌ Çalışmıyor"
echo ""
echo -n "   🌐 fxfutbol.com.tr: "
status=$(timeout 3 curl -s -o /dev/null -w "%{http_code}" https://fxfutbol.com.tr 2>/dev/null)
if [ "$status" = "200" ]; then
    echo "✅ OK (200)"
else
    echo "❌ Hata ($status)"
fi
echo ""

# 4. Son loglar
echo "4️⃣ Son loglar:"
echo ""
journalctl -u spradar.service -n 5 --no-pager
echo ""

echo "🎉 Tamamlandı!"
echo ""
echo "📌 Şimdi yapman gerekenler:"
echo "   1. Tarayıcıda Ctrl+Shift+R ile sayfayı yenile"
echo "   2. Yeni bir maça gir ve AI'ı test et"
echo ""
