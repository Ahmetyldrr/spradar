#!/bin/bash

# Spradar1 - Fixture2x Çalıştırma Scripti
echo "🚀 Fixture2x Sistemi Başlatılıyor..."
echo "==================================="

# Virtual environment'ı aktifleştir
source /home/ahmet/Desktop/Spradar1/venv/bin/activate

# Python modül olarak çalıştır (relative import sorununu çözer)
cd /home/ahmet/Desktop/Spradar1
python -m modules.fixture2x.main

echo ""
echo "🎯 İşlem tamamlandı!"