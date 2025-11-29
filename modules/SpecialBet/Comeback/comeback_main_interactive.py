#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 COMEBACK ANALYSIS MAIN - İNTERAKTİF VERSİYON
================================================

Kullanıcıdan tarih aralığı ister ve comeback analizi yapar.

Kullanım:
    # Manuel mod (tarih sorar):
    python comeback_main_interactive.py
    
    # Otomatik mod (bugün + 2 gün = 3 gün):
    python comeback_main_interactive.py --auto
    
    Manuel örnekler:
    Başlangıç: 05/11/25
    Bitiş: 07/11/25  → 3 günü birlikte işler
    
    Başlangıç: 06/11/25
    Bitiş: Enter     → Sadece 06/11/25'i işler

Version: 2.0 - Otomatik Cron Desteği + Log Sistemi
Date: November 9, 2025
"""

import sys
import os
import argparse
import traceback
sys.path.append('/home/ahmet/Desktop/Spradar1')

from database.source_connection import SourceConnection
from database.analytics_connection import AnalyticsConnection
from modules.SpecialBet.Comeback.comprehensive_comeback_commentary import generate_comprehensive_comeback_commentary
import pandas as pd
from datetime import datetime, timedelta
import json

# Log dosyası ayarı
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "comeback_cron.log")

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
    banner = "\n" + "="*80 + "\n"
    banner += "🔄 COMEBACK ANALYSIS SYSTEM - İNTERAKTİF MOD\n"
    banner += "="*80 + "\n"
    banner += "📊 Team_sum_last_10 Tablosu (286 Sütun)\n"
    banner += "🤖 AI-Ready Comprehensive Commentary\n"
    banner += "💾 PostgreSQL - comprehensive_comeback_analysis\n"
    banner += "="*80 + "\n"
    print(banner)


def get_date_range_interactive():
    """İnteraktif mod - kullanıcıdan tarih aralığı iste"""
    log_message("📅 MANUEL MOD - Tarih aralığı bekleniyor...")
    print("📅 BAŞLANGIÇ TARİHİ (DD/MM/YY formatında, örn: 05/11/25)")
    print("   Enter = Sadece bugünün tarihi kullanılır")
    start_date_input = input("➡️  Başlangıç: ").strip()
    
    if start_date_input:
        start_date = start_date_input
        print("\n📅 BİTİŞ TARİHİ (DD/MM/YY formatında, örn: 07/11/25)")
        print("   Enter = Sadece başlangıç tarihi işlenir")
        end_date_input = input("➡️  Bitiş: ").strip()
        
        if end_date_input:
            end_date = end_date_input
        else:
            end_date = start_date
    else:
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


def get_team_stats(analytics_db, team_id):
    """Team_sum_last_10'dan takım istatistiklerini çek"""
    query = """
        SELECT * FROM team_sum_last_10
        WHERE team_id = %s
    """
    df = analytics_db.query_df(query, params=(int(team_id),))
    
    if df is None or len(df) == 0:
        return None
    
    return df.iloc[0].to_dict()


def get_matches_by_date_range(source_db, start_date, end_date=None):
    """
    Tarih aralığındaki maçları çek
    
    Args:
        source_db: Veritabanı bağlantısı
        start_date: Başlangıç tarihi (DD/MM/YY)
        end_date: Bitiş tarihi (DD/MM/YY), None ise sadece start_date
    
    Returns:
        DataFrame: Maçlar
    """
    if end_date is None or end_date == start_date:
        # Tek tarih
        query = """
            SELECT match_id, season_id, home_team_id, home_team_name,
                   away_team_id, away_team_name, country_name, tournament_name,
                   match_date, match_time, round, week
            FROM public.current_week_fixtures
            WHERE match_date = %s
            ORDER BY match_date, match_time
        """
        return source_db.query_df(query, params=(start_date,))
    else:
        # Tarih aralığı
        query = """
            SELECT match_id, season_id, home_team_id, home_team_name,
                   away_team_id, away_team_name, country_name, tournament_name,
                   match_date, match_time, round, week
            FROM public.current_week_fixtures
            WHERE match_date BETWEEN %s AND %s
            ORDER BY match_date, match_time
        """
        return source_db.query_df(query, params=(start_date, end_date))


def main():
    """Ana program"""
    start_time = datetime.now()
    
    # Argparse setup
    parser = argparse.ArgumentParser(
        description='Comeback Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Kullanım Örnekleri:
  python comeback_main_interactive.py              # Manuel mod (tarih sorar)
  python comeback_main_interactive.py --auto       # Otomatik mod (bugün + 2 gün)
        """
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Otomatik mod: Bugün + 2 gün (toplam 3 gün) işler'
    )
    
    args = parser.parse_args()
    
    # Auto modda log dosyasını temizle
    if args.auto and os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'w') as f:
                f.write("")  # Dosyayı temizle
        except Exception as e:
            pass  # Hata olsa bile devam et
    
    # Log başlat
    log_message("="*80)
    log_message("🔄 COMEBACK ANALYSIS SYSTEM BAŞLADI")
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
        source_db = SourceConnection()
        analytics_db = AnalyticsConnection()
        log_message("✅ Bağlantılar başarılı!")
        
        # Maçları çek
        if end_date != start_date:
            log_message(f"📊 {start_date} - {end_date} tarih aralığındaki maçlar yükleniyor...")
            matches_df = get_matches_by_date_range(source_db, start_date, end_date)
        else:
            log_message(f"📊 {start_date} tarihindeki maçlar yükleniyor...")
            matches_df = get_matches_by_date_range(source_db, start_date, None)
        
        if matches_df is None or len(matches_df) == 0:
            log_message("❌ Seçilen tarihte/aralıkta maç bulunamadı!", "ERROR")
            return 1
        
        log_message(f"✅ {len(matches_df)} maç bulundu!")
        
        # Auto modda onay isteme
        if not args.auto:
            log_message(f"⚠️  {len(matches_df)} maç analiz edilecek. Bu işlem uzun sürebilir.", "WARNING")
            confirm = input("➡️  Devam etmek istiyor musunuz? (E/H): ").strip().upper()
            
            if confirm not in ['E', 'EVET', 'Y', 'YES']:
                log_message("❌ İşlem iptal edildi.", "WARNING")
                return 0
        
        log_message("="*80)
        log_message("🔄 Kapsamlı comeback analizleri yapılıyor...")
        log_message("="*80)
        
        results = []
        processed_count = 0
        skipped_count = 0
        
        for idx, row in matches_df.iterrows():
            log_message(f"📊 Maç {idx+1}/{len(matches_df)}: {row['home_team_name']} vs {row['away_team_name']}")
            
            # Takım istatistiklerini çek
            home_stats = get_team_stats(analytics_db, int(row['home_team_id']))
            away_stats = get_team_stats(analytics_db, int(row['away_team_id']))
            
            if home_stats is None or away_stats is None:
                log_message(f"   ⚠️  Veri yok, atlanıyor...", "WARNING")
                skipped_count += 1
                continue
            
            # Maç bilgilerini hazırla
            match_info = {
                'match_id': int(row['match_id']),
                'season_id': int(row['season_id']),
                'match_date': row['match_date'],
                'match_time': row['match_time'],
                'home_team_id': int(row['home_team_id']),
                'home_team_name': row['home_team_name'],
                'away_team_id': int(row['away_team_id']),
                'away_team_name': row['away_team_name'],
                'league': row['tournament_name'],
                'country': row['country_name']
            }
            
            # Kapsamlı commentary oluştur
            commentary_data = generate_comprehensive_comeback_commentary(home_stats, away_stats, match_info)
            
            # Comeback skorlarını hesapla
            home_comeback_win = int(home_stats.get('sum_all_sum_comeback_win', 0))
            home_comeback_draw = int(home_stats.get('sum_all_sum_comeback_draw', 0))
            home_matches = int(home_stats.get('sum_all_matches_played', 0))
            
            away_comeback_win = int(away_stats.get('sum_all_sum_comeback_win', 0))
            away_comeback_draw = int(away_stats.get('sum_all_sum_comeback_draw', 0))
            away_matches = int(away_stats.get('sum_all_matches_played', 0))
            
            # Comeback score: Total comeback / matches * 100
            home_comeback_score = ((home_comeback_win + home_comeback_draw) / home_matches * 100) if home_matches > 0 else 0
            away_comeback_score = ((away_comeback_win + away_comeback_draw) / away_matches * 100) if away_matches > 0 else 0
            
            # Combined comeback score (her iki takımın ortalaması)
            combined_comeback_score = (home_comeback_score + away_comeback_score) / 2
            
            # Data quality check
            data_quality = 'OK' if (home_matches >= 10 and away_matches >= 10) else 'INCOMPLETE'
            
            # Veritabanı için result hazırla
            result = {
                'match_id': int(row['match_id']),
                'season_id': int(row['season_id']),
                'match_date': row['match_date'],
                'match_time': row['match_time'],
                'home_team_id': int(row['home_team_id']),
                'home_team_name': row['home_team_name'],
                'away_team_id': int(row['away_team_id']),
                'away_team_name': row['away_team_name'],
                'country': row['country_name'],
                'league': row['tournament_name'],
                'round': float(row['round']) if row['round'] else None,
                'week': int(row['week']) if row['week'] else None,
                'home_matches_count': home_matches,
                'away_matches_count': away_matches,
                'home_comeback_score': round(home_comeback_score, 2),
                'away_comeback_score': round(away_comeback_score, 2),
                'combined_comeback_score': round(combined_comeback_score, 2),
                'data_quality': data_quality,
                'commentary_json': json.dumps(commentary_data, ensure_ascii=False),
                'created_at': datetime.now()
            }
            
            results.append(result)
            processed_count += 1
            
            # İstatistik özeti
            prompt_length = len(commentary_data['combined_prompt'])
            log_message(f"   ✅ Commentary: {prompt_length:,} karakter | Comeback Score: {combined_comeback_score:.1f} | Quality: {data_quality}")
        
        if len(results) == 0:
            log_message("❌ İşlenebilir maç bulunamadı!", "ERROR")
            return 1
        
        results_df = pd.DataFrame(results)
        log_message(f"✅ Toplam {len(results_df)} maç analiz edildi! ({skipped_count} atlandı)")
        
        # Combined comeback score'a göre BÜYÜKTEN KÜÇÜĞE sırala
        log_message("🔄 Maçlar comeback skoruna göre sıralanıyor...")
        results_df = results_df.sort_values('combined_comeback_score', ascending=False)
        log_message("✅ Sıralama tamamlandı!")
        
        log_message("💾 Veriler sr_analiz_db'ye kaydediliyor...")
        table_name = 'comprehensive_comeback_analysis'
        success = analytics_db.bulk_df(results_df, table_name, replace=True)
        
        if success:
            log_message(f"✅ {table_name} tablosuna {len(results_df)} kayıt eklendi!")
            
            # Data quality özeti
            ok_count = len(results_df[results_df['data_quality'] == 'OK'])
            incomplete_count = len(results_df[results_df['data_quality'] == 'INCOMPLETE'])
            log_message("="*80)
            log_message("📊 VERİ KALİTESİ:")
            log_message(f"   ✅ OK (10+ maç): {ok_count} maç ({ok_count/len(results_df)*100:.1f}%)")
            log_message(f"   ⚠️  INCOMPLETE (<10 maç): {incomplete_count} maç ({incomplete_count/len(results_df)*100:.1f}%)")
            
            # En yüksek comeback skorları
            log_message("="*80)
            log_message("🔥 EN YÜKSEK COMEBACK POTANSİYELLİ MAÇLAR (Combined Score):")
            top_matches = results_df.nlargest(10, 'combined_comeback_score')[
                ['home_team_name', 'away_team_name', 'combined_comeback_score', 
                 'home_comeback_score', 'away_comeback_score', 'data_quality', 
                 'match_date', 'match_time', 'league']
            ]
            for idx, r in top_matches.iterrows():
                quality_icon = "✅" if r['data_quality'] == 'OK' else "⚠️"
                log_message(f"   {quality_icon} {r['home_team_name']} vs {r['away_team_name']}")
                log_message(f"      🔥 Combined: {r['combined_comeback_score']:.1f} | Ev: {r['home_comeback_score']:.1f} | Dep: {r['away_comeback_score']:.1f}")
                log_message(f"      🏆 {r['league']}")
                log_message(f"      📅 {r['match_date']} {r['match_time']}")
            
            # İlk maçın commentary preview
            log_message("="*80)
            log_message("📄 ÖRNEK COMMENTARY (En Yüksek Skorlu Maç):")
            log_message("="*80)
            first_commentary = json.loads(results_df.iloc[0]['commentary_json'])
            preview = first_commentary['combined_prompt'][:500]
            log_message(preview + "...")
            
            # Özet
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            log_message("="*80)
            log_message("✅ İŞLEM TAMAMLANDI!", "SUCCESS")
            log_message("="*80)
            log_message(f"� İşlenen Maç Sayısı: {len(results_df)}")
            log_message(f"⏭️  Atlanan Maç Sayısı: {skipped_count}")
            log_message(f"💾 Veritabanı: comprehensive_comeback_analysis")
            log_message(f"📅 Tarih Aralığı: {start_date} - {end_date}")
            log_message(f"⏰ Süre: {duration:.2f} saniye")
            log_message("="*80)
            
            return 0
        else:
            log_message("❌ Kaydetme başarısız!", "ERROR")
            return 1
        
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
