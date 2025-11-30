#!/bin/bash
set -e  # Hata olursa dur

echo "🚀 SPRADAR DOCKER COMPOSE KURULUMU"
echo "===================================="
echo ""

# Renkler
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Docker kontrolü
echo -e "${YELLOW}1️⃣ Docker kontrolü...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker yüklü değil! Yükleniyor...${NC}"
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker yüklendi${NC}"
else
    echo -e "${GREEN}✅ Docker mevcut${NC}"
fi

# 2. Docker Compose kontrolü
echo ""
echo -e "${YELLOW}2️⃣ Docker Compose kontrolü...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose yüklü değil! Yükleniyor...${NC}"
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose yüklendi${NC}"
else
    echo -e "${GREEN}✅ Docker Compose mevcut${NC}"
fi

# 3. .env.docker kontrolü
echo ""
echo -e "${YELLOW}3️⃣ .env.docker kontrolü...${NC}"
if [ ! -f ".env.docker" ]; then
    echo -e "${RED}❌ .env.docker bulunamadı!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ .env.docker mevcut${NC}"

# 4. Mevcut servisleri durdur
echo ""
echo -e "${YELLOW}4️⃣ Mevcut servisleri durduruluyor...${NC}"
sudo systemctl stop spradar.service 2>/dev/null || true
sudo docker stop personal_nginx 2>/dev/null || true
sleep 2
echo -e "${GREEN}✅ Eski servisler durduruldu${NC}"

# 5. Eski nginx container'ı sil
echo ""
echo -e "${YELLOW}5️⃣ Eski nginx container temizleniyor...${NC}"
sudo docker rm personal_nginx 2>/dev/null || true
echo -e "${GREEN}✅ Temizlendi${NC}"

# 6. Docker build
echo ""
echo -e "${YELLOW}6️⃣ Docker imajları build ediliyor...${NC}"
echo -e "${YELLOW}   (İlk seferde 2-3 dakika sürebilir)${NC}"
docker-compose build --no-cache
echo -e "${GREEN}✅ Build tamamlandı${NC}"

# 7. Containerları başlat
echo ""
echo -e "${YELLOW}7️⃣ Containerlar başlatılıyor...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Containerlar başlatıldı${NC}"

# 8. Durum kontrolü
echo ""
echo -e "${YELLOW}8️⃣ Servis durumu kontrol ediliyor...${NC}"
sleep 5
docker-compose ps
echo ""

# 9. Sağlık kontrolü
echo -e "${YELLOW}9️⃣ Sağlık kontrolü...${NC}"
sleep 5

# Web container kontrolü
if docker-compose ps | grep spradar_web | grep -q "Up"; then
    echo -e "${GREEN}✅ Django/Gunicorn çalışıyor${NC}"
else
    echo -e "${RED}❌ Django/Gunicorn başlatılamadı${NC}"
    docker-compose logs web
    exit 1
fi

# Nginx container kontrolü
if docker-compose ps | grep spradar_nginx | grep -q "Up"; then
    echo -e "${GREEN}✅ Nginx çalışıyor${NC}"
else
    echo -e "${RED}❌ Nginx başlatılamadı${NC}"
    docker-compose logs nginx
    exit 1
fi

# 10. HTTP testi
echo ""
echo -e "${YELLOW}🔟 HTTP/HTTPS testi...${NC}"
sleep 2

if curl -s -o /dev/null -w "%{http_code}" http://localhost:8095 | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✅ HTTP çalışıyor${NC}"
else
    echo -e "${YELLOW}⚠️ HTTP henüz hazır değil, logları kontrol et${NC}"
fi

# 11. Son loglar
echo ""
echo -e "${YELLOW}1️⃣1️⃣ Son loglar:${NC}"
docker-compose logs --tail=30
echo ""

# 12. Özet
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 KURULUM TAMAMLANDI!${NC}"
echo "=========================================="
echo ""
echo -e "${GREEN}📊 Durum Komutları:${NC}"
echo "   docker-compose ps              - Container durumu"
echo "   docker-compose logs -f         - Canlı loglar"
echo "   docker-compose logs web        - Django logları"
echo "   docker-compose logs nginx      - Nginx logları"
echo ""
echo -e "${GREEN}🔄 Yönetim:${NC}"
echo "   bash docker-manage.sh restart  - Yeniden başlat"
echo "   bash docker-manage.sh stop     - Durdur"
echo "   bash docker-manage.sh logs     - Logları izle"
echo ""
echo -e "${GREEN}🌐 Test:${NC}"
echo "   curl http://localhost:8095     - Local test"
echo "   curl https://fxfutbol.com.tr   - Production test"
echo ""
echo -e "${YELLOW}⚠️ Önemli:${NC}"
echo "   Tarayıcıda Ctrl+Shift+R ile cache temizle!"
echo ""
