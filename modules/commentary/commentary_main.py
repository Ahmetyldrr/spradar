#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 COMMENTARY MAIN - ANA ÇALIŞTIRICI
====================================

İnteraktif olarak tarih aralığı sorar ve günlük maçları işleyip veritabanına kaydeder.

Kullanım:
    # Manuel mod (tarih sorar):
    python commentary_main.py
    
    # Otomatik mod (bugün + 2 gün = 3 gün):
    python commentary_main.py --auto
    
    Manuel örnekler:
    Başlangıç: 05/11/25
    Bitiş: 07/11/25  → 3 günü birlikte işler
    
    Başlangıç: 06/11/25
    Bitiş: Enter     → Sadece 06/11/25'i işler

Author: Spradar Analytics Team
Date: November 9, 2025
Version: 7.0 - Otomatik Cron Desteği + Log Sistemi
"""

import sys
import os
import argparse
import traceback
from datetime import datetime, timedelta

# Proje root'u path'e ekle
sys.path.append('/home/ahmet/Desktop/Spradar1')

from database.source_connection import SourceConnection
from database.analytics_connection import AnalyticsConnection
from modules.commentary.daily_matches import (
    process_daily_matches,
    clear_daily_commentaries_table,
    search_commentaries_by_date
)

# Log dosyası ayarı
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "commentary_cron.log")

def log_message(message, level="INFO"):
    """Log mesajı yaz"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    # Console'a da yazdır
    print(log_entry.strip())
    
    # Log dosyasına yaz
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


def print_banner():
    """Başlangıç banner'ı"""
    banner_text = "\n" + "=" * 80 + "\n"
    banner_text += "🎯 COMMENTARY SYSTEM - GÜNLÜK MAÇ ANALİZ SİSTEMİ\n"
    banner_text += "=" * 80 + "\n"
    banner_text += "📊 286 Sütunlu Team_sum_last_10 Tablosu\n"
    banner_text += "🤖 RAG/AI Optimized Commentary Generator\n"
    banner_text += "💾 PostgreSQL - daily_match_commentaries\n"
    banner_text += "=" * 80 + "\n"
    print(banner_text)


def get_date_range_interactive():
    """İnteraktif mod - kullanıcıdan tarih aralığı iste"""
    log_message("📅 MANUEL MOD - Tarih aralığı bekleniyor...")
    print("📅 BAŞLANGIÇ TARİHİ (DD/MM/YY formatında, örn: 05/11/25)")
    print("   Enter = Sadece bugünün tarihi kullanılır")
    start_date_input = input("➡️  Başlangıç: ").strip()
    
    # Başlangıç tarihi belirle
    if start_date_input:
        start_date = start_date_input
        
        # Bitiş tarihini sor
        print("\n📅 BİTİŞ TARİHİ (DD/MM/YY formatında, örn: 07/11/25)")
        print("   Enter = Sadece başlangıç tarihi işlenir")
        end_date_input = input("➡️  Bitiş: ").strip()
        
        if end_date_input:
            end_date = end_date_input
        else:
            end_date = start_date
    else:
        # Tarih belirtilmedi, bugünü kullan
        start_date = datetime.now().strftime('%d/%m/%y')
        end_date = start_date
        log_message(f"⚠️  Tarih belirtilmedi, bugün kullanılıyor: {start_date}", "WARNING")
    
    return start_date, end_date


def get_date_range_auto():
    """Otomatik mod - bugün + 2 gün (toplam 3 gün)"""
    log_message("🤖 OTOMATİK MOD - Bugün + 2 gün (toplam 3 gün)")
    
    today = datetime.now()
    start_date = today.strftime('%d/%m/%y')
    end_date = (today + timedelta(days=2)).strftime('%d/%m/%y')
    
    log_message(f"📅 Tarih aralığı: {start_date} - {end_date}")
    
    return start_date, end_date


def process_date_range(source_db, analytics_db, start_date, end_date, save_to_db=True):
    """Tarih aralığındaki tüm maçları işle"""
    
    # Tarihleri parse et - hem 2 haneli hem 4 haneli yılı destekle
    try:
        start_dt = datetime.strptime(start_date, '%d/%m/%y')
    except ValueError:
        start_dt = datetime.strptime(start_date, '%d/%m/%Y')
    
    try:
        end_dt = datetime.strptime(end_date, '%d/%m/%y')
    except ValueError:
        end_dt = datetime.strptime(end_date, '%d/%m/%Y')
    
    # Aynı tarih mi kontrol et
    is_same_date = (start_dt == end_dt)
    
    if is_same_date:
        log_message(f"📅 Tek tarih işlenecek: {start_date}")
        # Tek tarih işle
        commentaries = process_daily_matches(
            source_db=source_db,
            analytics_db=analytics_db,
            match_date=start_date,
            table_name='team_sum_last_10',
            save_to_db=save_to_db
        )
        
        if not commentaries:
            log_message(f"❌ {start_date} tarihinde maç bulunamadı!", "ERROR")
            return None
        
        log_message(f"✅ {len(commentaries)} maç işlendi!", "SUCCESS")
        return commentaries
    
    else:
        log_message(f"📅 Tarih aralığı işlenecek: {start_date} - {end_date}")
        # Çoklu tarih işle
        current_dt = start_dt
        total_commentaries = []
        
        while current_dt <= end_dt:
            current_date_str = current_dt.strftime('%d/%m/%y')
            log_message("="*80)
            log_message(f"📅 İŞLENİYOR: {current_date_str}")
            log_message("="*80)
            
            # Bu tarih için maçları işle
            commentaries = process_daily_matches(
                source_db=source_db,
                analytics_db=analytics_db,
                match_date=current_date_str,
                table_name='team_sum_last_10',
                save_to_db=save_to_db
            )
            
            if commentaries:
                total_commentaries.extend(commentaries)
                log_message(f"✅ {current_date_str}: {len(commentaries)} maç işlendi", "SUCCESS")
            else:
                log_message(f"⚠️  {current_date_str}: Maç bulunamadı", "WARNING")
            
            # Bir sonraki güne geç
            current_dt += timedelta(days=1)
        
        if not total_commentaries:
            log_message(f"❌ {start_date} - {end_date} aralığında maç bulunamadı!", "ERROR")
            return None
        
        log_message(f"✅ TOPLAM {len(total_commentaries)} maç işlendi! ({start_date} - {end_date})", "SUCCESS")
        return total_commentaries


def main():
    """Ana program"""
    start_time = datetime.now()
    
    # Argparse setup
    parser = argparse.ArgumentParser(
        description='Commentary System - Günlük Maç Analiz Sistemi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Kullanım Örnekleri:
  python commentary_main.py              # Manuel mod (tarih sorar)
  python commentary_main.py --auto       # Otomatik mod (bugün + 2 gün)
        """
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Otomatik mod: Bugün + 2 gün (toplam 3 gün) işler'
    )
    
    args = parser.parse_args()
    
    # Log başlat
    log_message("="*80)
    log_message("🎯 COMMENTARY SYSTEM BAŞLADI")
    log_message("="*80)
    
    try:
        # Banner göster
        print_banner()
        
        # Tarih aralığını belirle (otomatik veya manuel)
        if args.auto:
            start_date, end_date = get_date_range_auto()
        else:
            start_date, end_date = get_date_range_interactive()
        
        # Tarih aralığını göster
        log_message(f"📅 İşlenecek Tarih Aralığı: {start_date} - {end_date}")
        log_message(f"⏰ İşlem Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_message("="*80)
        
        # Veritabanı bağlantıları
        log_message("🔌 Veritabanı bağlantıları kuruluyor...")
        analytics_db = AnalyticsConnection()
        source_db = SourceConnection()
        log_message("✅ Bağlantılar başarılı!", "SUCCESS")
        
        # Tablo temizle
        log_message("🗑️  Önceki yorumlar temizleniyor...")
        if clear_daily_commentaries_table(analytics_db):
            log_message("✅ Tablo başarıyla temizlendi!", "SUCCESS")
        else:
            log_message("❌ Tablo temizleme başarısız!", "ERROR")
            return 1
        
        # Maçları işle
        log_message("💾 Maçlar işlenip veritabanına kaydediliyor...")
        log_message("="*80)
        
        commentaries = process_date_range(
            source_db=source_db,
            analytics_db=analytics_db,
            start_date=start_date,
            end_date=end_date,
            save_to_db=True
        )
        
        if not commentaries:
            log_message("❌ İşlenecek maç bulunamadı!", "ERROR")
            return 1
        
        # Sonuçları göster
        log_message("="*80)
        log_message("📋 KAYDEDİLEN MAÇLAR - ÖZET")
        log_message("="*80)
        
        # Tarihleri parse et
        start_dt = datetime.strptime(start_date, '%d/%m/%y')
        end_dt = datetime.strptime(end_date, '%d/%m/%y')
        is_same_date = (start_dt == end_dt)
        
        # Veritabanından kaydedilmiş maçları çek
        if is_same_date:
            saved_matches = search_commentaries_by_date(analytics_db, start_date)
        else:
            query = f"""
            SELECT * FROM daily_match_commentaries 
            WHERE match_date BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY match_date, match_time
            """
            saved_matches = analytics_db.query_df(query)
        
        if saved_matches is not None and len(saved_matches) > 0:
            log_message(f"✅ Toplam {len(saved_matches)} maç kaydı bulundu", "SUCCESS")
            
            for idx, row in saved_matches.iterrows():
                json_data = row['commentary_json']
                combined_length = len(json_data.get('combined_prompt', ''))
                
                match_info = f"MAÇ #{idx + 1}: {row['home_team_name']} vs {row['away_team_name']} | " \
                            f"{row['country']} - {row['league']} | {row['match_time']} | " \
                            f"Prompt: {combined_length:,} karakter"
                log_message(match_info)
        else:
            log_message("❌ Kaydedilmiş maç bulunamadı!", "ERROR")
        
        # Özet
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        log_message("="*80)
        log_message("✅ İŞLEM TAMAMLANDI!", "SUCCESS")
        log_message("="*80)
        log_message(f"📊 İşlenen Maç Sayısı: {len(commentaries)}")
        log_message(f"💾 Veritabanı: daily_match_commentaries")
        log_message(f"📅 Tarih Aralığı: {start_date} - {end_date}")
        log_message(f"⏰ Süre: {duration:.2f} saniye")
        log_message("="*80)
        
        return 0
        
    except KeyboardInterrupt:
        log_message("⚠️  İşlem kullanıcı tarafından iptal edildi!", "WARNING")
        return 130
        
    except Exception as e:
        log_message("="*80, "ERROR")
        log_message(f"❌ HATA OLUŞTU: {str(e)}", "ERROR")
        log_message("="*80, "ERROR")
        log_message("Detaylı hata bilgisi:", "ERROR")
        log_message(traceback.format_exc(), "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())
