#!/bin/bash
# 🚀 Docker Compose Hızlı Başlangıç

echo "🐳 Spradar Docker Compose Kurulumu"
echo "===================================="
echo ""

# Kontroller
echo "1️⃣ Docker kontrolü..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker yüklü değil!"
    echo "Yüklemek için: curl -fsSL https://get.docker.com | sh"
    exit 1
fi
echo "✅ Docker mevcut"

echo ""
echo "2️⃣ Docker Compose kontrolü..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose yüklü değil!"
    exit 1
fi
echo "✅ Docker Compose mevcut"

echo ""
echo "3️⃣ .env.docker dosyası kontrolü..."
if [ ! -f ".env.docker" ]; then
    echo "❌ .env.docker dosyası bulunamadı!"
    echo "Lütfen .env.docker dosyasını oluşturun."
    exit 1
fi
echo "✅ .env.docker mevcut"

echo ""
echo "4️⃣ Mevcut servisleri durdur..."
sudo systemctl stop spradar.service 2>/dev/null || true
sudo docker stop personal_nginx 2>/dev/null || true
echo "✅ Eski servisler durduruldu"

echo ""
echo "5️⃣ Docker imajları build ediliyor..."
echo "   (İlk seferde 2-3 dakika sürebilir)"
docker-compose build

echo ""
echo "6️⃣ Containerlar başlatılıyor..."
docker-compose up -d

echo ""
echo "7️⃣ Servis durumu kontrol ediliyor..."
sleep 5
docker-compose ps

echo ""
echo "8️⃣ Loglar kontrol ediliyor..."
docker-compose logs --tail=20

echo ""
echo "=========================================="
echo "🎉 Kurulum tamamlandı!"
echo ""
echo "📊 Durum kontrolü:"
echo "   docker-compose ps"
echo ""
echo "📋 Logları izle:"
echo "   docker-compose logs -f"
echo ""
echo "🔄 Yeniden başlat:"
echo "   bash docker-manage.sh restart"
echo ""
echo "🌐 Test et:"
echo "   curl https://fxfutbol.com.tr"
echo ""
