#!/bin/bash

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script bilgileri
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"
LOG_FILE="$SCRIPT_DIR/fixture2x_cron.log"

# Python executable path (virtual environment)
PYTHON_PATH="/home/ahmet/Desktop/Spradar1/.venv/bin/python3"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🕒 FIXTURE 2X - CRON JOB KURULUMU${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Python script kontrolü
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Hata: main.py bulunamadı!${NC}"
    echo -e "${RED}Aranılan: $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Python kontrolü
if [ ! -f "$PYTHON_PATH" ]; then
    echo -e "${RED}❌ Hata: Python executable bulunamadı!${NC}"
    echo -e "${RED}Aranılan: $PYTHON_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python script: $PYTHON_SCRIPT${NC}"
echo -e "${GREEN}✅ Python path: $PYTHON_PATH${NC}"
echo -e "${GREEN}✅ Log dosyası: $LOG_FILE${NC}\n"

# Cron job tanımı
CRON_COMMAND="30 0 * * * cd $SCRIPT_DIR && $PYTHON_PATH $PYTHON_SCRIPT >> $LOG_FILE 2>&1"

# Mevcut crontab'ı kontrol et
echo -e "${YELLOW}🔍 Mevcut cron job'lar kontrol ediliyor...${NC}"
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$PYTHON_SCRIPT")

if [ ! -z "$EXISTING_CRON" ]; then
    echo -e "${YELLOW}⚠️  Bu script için zaten bir cron job var:${NC}"
    echo -e "${YELLOW}   $EXISTING_CRON${NC}\n"
    
    read -p "Mevcut cron job'ı silip yenisini eklemek ister misiniz? (E/h): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Ee]$ ]]; then
        # Eski cron job'ı sil
        (crontab -l 2>/dev/null | grep -v -F "$PYTHON_SCRIPT") | crontab -
        echo -e "${GREEN}✅ Eski cron job silindi${NC}"
    else
        echo -e "${BLUE}ℹ️  İşlem iptal edildi${NC}"
        exit 0
    fi
fi

# Yeni cron job ekle
echo -e "${YELLOW}📝 Yeni cron job ekleniyor...${NC}"
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cron job başarıyla eklendi!${NC}\n"
    
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}📋 CRON JOB BİLGİLERİ${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "${GREEN}Çalışma Saati:${NC} Her gün 00:30"
    echo -e "${GREEN}Script:${NC} $PYTHON_SCRIPT"
    echo -e "${GREEN}Log Dosyası:${NC} $LOG_FILE"
    echo -e "${BLUE}================================================${NC}\n"
    
    echo -e "${YELLOW}💡 Logları görmek için:${NC}"
    echo -e "   ./view_logs.sh tail    ${BLUE}# Son 50 satır${NC}"
    echo -e "   ./view_logs.sh live    ${BLUE}# Canlı takip${NC}"
    echo -e "   ./view_logs.sh today   ${BLUE}# Bugünün logları${NC}\n"
    
    # İlk çalıştırma testi öner
    read -p "Script'i şimdi test etmek ister misiniz? (E/h): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Ee]$ ]]; then
        echo -e "${YELLOW}🚀 Test çalıştırması başlatılıyor...${NC}\n"
        cd "$SCRIPT_DIR"
        $PYTHON_PATH "$PYTHON_SCRIPT"
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}✅ Test başarılı!${NC}"
        else
            echo -e "\n${RED}❌ Test başarısız! Lütfen logları kontrol edin.${NC}"
        fi
    fi
    
else
    echo -e "${RED}❌ Cron job eklenirken hata oluştu!${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 Kurulum tamamlandı!${NC}"
