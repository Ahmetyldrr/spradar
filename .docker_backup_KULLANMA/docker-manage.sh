#!/bin/bash
# 🐳 Docker Compose ile Spradar Yönetimi

case "$1" in
    start)
        echo "🚀 Spradar başlatılıyor..."
        docker-compose up -d
        echo "✅ Başlatıldı!"
        echo "📊 Durum: docker-compose ps"
        docker-compose ps
        ;;
    
    stop)
        echo "🛑 Spradar durduruluyor..."
        docker-compose down
        echo "✅ Durduruldu!"
        ;;
    
    restart)
        echo "🔄 Spradar yeniden başlatılıyor..."
        docker-compose down
        sleep 2
        docker-compose up -d
        echo "✅ Yeniden başlatıldı!"
        docker-compose ps
        ;;
    
    rebuild)
        echo "🏗️ Spradar yeniden build ediliyor..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo "✅ Rebuild tamamlandı!"
        docker-compose ps
        ;;
    
    logs)
        echo "📋 Loglar gösteriliyor..."
        docker-compose logs -f --tail=50
        ;;
    
    status)
        echo "📊 Spradar durumu:"
        docker-compose ps
        ;;
    
    clean)
        echo "🧹 Tüm containerlar ve volumeler temizleniyor..."
        read -p "Emin misin? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            docker system prune -f
            echo "✅ Temizlendi!"
        fi
        ;;
    
    shell)
        echo "🐚 Django shell açılıyor..."
        docker-compose exec web python manage.py shell
        ;;
    
    migrate)
        echo "🗄️ Migrationlar çalıştırılıyor..."
        docker-compose exec web python manage.py migrate
        echo "✅ Migrationlar tamamlandı!"
        ;;
    
    *)
        echo "🐳 Spradar Docker Yönetim Scripti"
        echo ""
        echo "Kullanım: sudo bash docker-manage.sh [komut]"
        echo ""
        echo "Komutlar:"
        echo "  start     - Tüm servisleri başlat"
        echo "  stop      - Tüm servisleri durdur"
        echo "  restart   - Tüm servisleri yeniden başlat (⚡ EN ÇOK KULLANILAN)"
        echo "  rebuild   - Sıfırdan build et ve başlat"
        echo "  logs      - Canlı logları göster"
        echo "  status    - Container durumlarını göster"
        echo "  clean     - Tüm containerları ve volumeleri temizle"
        echo "  shell     - Django shell'e gir"
        echo "  migrate   - Database migrationlarını çalıştır"
        echo ""
        echo "Örnek:"
        echo "  sudo bash docker-manage.sh restart  ← AI kodu değiştirdiysen"
        echo ""
        ;;
esac
