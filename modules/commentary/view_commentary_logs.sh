#!/bin/bash

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Log dosyası
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/commentary_cron.log"

# Log dosyası kontrolü
if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}❌ Log dosyası bulunamadı: $LOG_FILE${NC}"
    exit 1
fi

# Kullanım fonksiyonu
usage() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}📋 COMMENTARY LOG GÖRÜNTÜLEYICI - KULLANIM${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "${GREEN}Kullanım:${NC} ./view_commentary_logs.sh [komut]"
    echo ""
    echo -e "${YELLOW}Komutlar:${NC}"
    echo -e "  ${CYAN}tail${NC}      - Son 50 satırı göster"
    echo -e "  ${CYAN}live${NC}      - Canlı log takibi (CTRL+C ile çık)"
    echo -e "  ${CYAN}errors${NC}    - Sadece hataları göster"
    echo -e "  ${CYAN}success${NC}   - Başarılı işlemleri göster"
    echo -e "  ${CYAN}today${NC}     - Bugünün loglarını göster"
    echo -e "  ${CYAN}stats${NC}     - Log istatistikleri"
    echo -e "  ${CYAN}all${NC}       - Tüm logları göster"
    echo ""
    echo -e "${YELLOW}Örnekler:${NC}"
    echo -e "  ./view_commentary_logs.sh tail"
    echo -e "  ./view_commentary_logs.sh live"
    echo -e "  ./view_commentary_logs.sh errors"
    echo -e "${BLUE}================================================${NC}"
}

# Parametre kontrolü
if [ $# -eq 0 ]; then
    usage
    exit 0
fi

COMMAND=$1

case $COMMAND in
    tail)
        echo -e "${BLUE}📄 Son 50 satır:${NC}\n"
        tail -n 50 "$LOG_FILE"
        ;;
    
    live)
        echo -e "${BLUE}📡 Canlı log takibi (CTRL+C ile çık)${NC}\n"
        tail -f "$LOG_FILE"
        ;;
    
    errors)
        echo -e "${RED}❌ Hatalar:${NC}\n"
        grep -i "ERROR" "$LOG_FILE" | tail -n 50
        if [ $? -ne 0 ]; then
            echo -e "${GREEN}✅ Hata kaydı bulunamadı!${NC}"
        fi
        ;;
    
    success)
        echo -e "${GREEN}✅ Başarılı işlemler:${NC}\n"
        grep -i "SUCCESS\|başarılı\|tamamlandi" "$LOG_FILE" | tail -n 50
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}⚠️  Başarılı işlem kaydı bulunamadı!${NC}"
        fi
        ;;
    
    today)
        TODAY=$(date +%Y-%m-%d)
        echo -e "${BLUE}📅 Bugünün logları ($TODAY):${NC}\n"
        grep "$TODAY" "$LOG_FILE"
        if [ $? -ne 0 ]; then
            echo -e "${YELLOW}⚠️  Bugün için log bulunamadı!${NC}"
        fi
        ;;
    
    stats)
        echo -e "${BLUE}================================================${NC}"
        echo -e "${BLUE}📊 COMMENTARY LOG İSTATİSTİKLERİ${NC}"
        echo -e "${BLUE}================================================${NC}"
        
        TOTAL_LINES=$(wc -l < "$LOG_FILE")
        ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null || echo "0")
        SUCCESS_COUNT=$(grep -c "SUCCESS" "$LOG_FILE" 2>/dev/null || echo "0")
        
        # İlk ve son log tarihleri
        FIRST_LOG=$(head -n 1 "$LOG_FILE" | grep -oP '\[\K[^\]]+' | head -n 1)
        LAST_LOG=$(tail -n 1 "$LOG_FILE" | grep -oP '\[\K[^\]]+' | head -n 1)
        
        echo -e "${GREEN}Toplam Satır:${NC} $TOTAL_LINES"
        echo -e "${RED}Hata Sayısı:${NC} $ERROR_COUNT"
        echo -e "${GREEN}Başarılı İşlem:${NC} $SUCCESS_COUNT"
        echo ""
        echo -e "${CYAN}İlk Log:${NC} $FIRST_LOG"
        echo -e "${CYAN}Son Log:${NC} $LAST_LOG"
        echo ""
        echo -e "${YELLOW}Dosya Boyutu:${NC} $(du -h "$LOG_FILE" | cut -f1)"
        echo -e "${BLUE}================================================${NC}"
        ;;
    
    all)
        echo -e "${BLUE}📄 Tüm loglar:${NC}\n"
        cat "$LOG_FILE"
        ;;
    
    *)
        echo -e "${RED}❌ Bilinmeyen komut: $COMMAND${NC}\n"
        usage
        exit 1
        ;;
esac
