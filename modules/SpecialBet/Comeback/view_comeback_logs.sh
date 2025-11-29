#!/bin/bash

# Comeback Log Viewer Script
# Comeback cron işlemlerinin loglarını görüntülemek için kullanılır

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/comeback_cron.log"

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_usage() {
    echo -e "${BLUE}Comeback Log Viewer${NC}"
    echo -e "Kullanım: $0 [komut]"
    echo ""
    echo "Komutlar:"
    echo "  tail       - Son 50 satırı göster (varsayılan)"
    echo "  live       - Canlı log takibi (tail -f)"
    echo "  errors     - Sadece hataları göster"
    echo "  success    - Sadece başarılı işlemleri göster"
    echo "  today      - Bugünün loglarını göster"
    echo "  stats      - İstatistikleri göster"
    echo "  clear      - Log dosyasını temizle"
    echo ""
}

show_tail() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}=== Son 50 Log Satırı ===${NC}"
        tail -50 "$LOG_FILE"
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

show_live() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}=== Canlı Log Takibi (Çıkmak için Ctrl+C) ===${NC}"
        tail -f "$LOG_FILE"
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

show_errors() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${RED}=== Hata Logları ===${NC}"
        grep -E "ERROR|HATA|❌" "$LOG_FILE" | tail -30
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

show_success() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${GREEN}=== Başarılı İşlemler ===${NC}"
        grep -E "SUCCESS|✅|İŞLEM TAMAMLANDI" "$LOG_FILE" | tail -20
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

show_today() {
    if [ -f "$LOG_FILE" ]; then
        TODAY=$(date +"%Y-%m-%d")
        echo -e "${BLUE}=== Bugünün Logları ($TODAY) ===${NC}"
        grep "$TODAY" "$LOG_FILE"
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

show_stats() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}=== Comeback Log İstatistikleri ===${NC}"
        echo ""
        
        TOTAL_LINES=$(wc -l < "$LOG_FILE")
        ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null || echo "0")
        SUCCESS_COUNT=$(grep -c "İŞLEM TAMAMLANDI" "$LOG_FILE" 2>/dev/null || echo "0")
        WARNING_COUNT=$(grep -c "WARNING" "$LOG_FILE" 2>/dev/null || echo "0")
        
        echo -e "📊 Toplam Satır: ${YELLOW}$TOTAL_LINES${NC}"
        echo -e "✅ Başarılı İşlem: ${GREEN}$SUCCESS_COUNT${NC}"
        echo -e "⚠️  Uyarı: ${YELLOW}$WARNING_COUNT${NC}"
        echo -e "❌ Hata: ${RED}$ERROR_COUNT${NC}"
        echo ""
        
        if [ -f "$LOG_FILE" ]; then
            FIRST_DATE=$(head -1 "$LOG_FILE" | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)
            LAST_DATE=$(tail -1 "$LOG_FILE" | grep -oP '\d{4}-\d{2}-\d{2}' | tail -1)
            
            if [ ! -z "$FIRST_DATE" ] && [ ! -z "$LAST_DATE" ]; then
                echo -e "📅 İlk Log: $FIRST_DATE"
                echo -e "📅 Son Log: $LAST_DATE"
            fi
        fi
        
        echo ""
        FILE_SIZE=$(du -h "$LOG_FILE" | cut -f1)
        echo -e "💾 Dosya Boyutu: $FILE_SIZE"
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

clear_logs() {
    if [ -f "$LOG_FILE" ]; then
        read -p "Log dosyasını temizlemek istediğinize emin misiniz? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            > "$LOG_FILE"
            echo -e "${GREEN}✅ Log dosyası temizlendi${NC}"
        else
            echo -e "${YELLOW}İşlem iptal edildi${NC}"
        fi
    else
        echo -e "${RED}Log dosyası bulunamadı: $LOG_FILE${NC}"
    fi
}

# Ana komut işleme
case "${1:-tail}" in
    tail)
        show_tail
        ;;
    live)
        show_live
        ;;
    errors)
        show_errors
        ;;
    success)
        show_success
        ;;
    today)
        show_today
        ;;
    stats)
        show_stats
        ;;
    clear)
        clear_logs
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        echo -e "${RED}Geçersiz komut: $1${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac
