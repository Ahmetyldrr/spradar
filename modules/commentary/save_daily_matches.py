#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 GÜNLÜK MAÇLARI VERİTABANINA KAYDET
=====================================

05/11/25 gibi bir tarih için o günün maçlarını işleyip
daily_match_commentaries tablosuna kaydeder.

Kullanım:
    python save_daily_matches.py 05/11/25
    python save_daily_matches.py 05/11/25 --clear  (önce tabloyu temizle)
    python save_daily_matches.py 05/11/25 --show   (kaydedilenleri göster)
    python save_daily_matches.py 05/11/25 --no-save  (sadece test, kaydetme)

Author: Spradar Analytics Team
Date: November 5, 2025
Version: 4.0 - Sadeleştirilmiş JSON Yapısı
"""

import sys
import argparse
from datetime import datetime

# Proje root'u path'e ekle
sys.path.append('/home/ahmet/Desktop/Spradar1')

from database.source_connection import SourceConnection
from database.analytics_connection import AnalyticsConnection
from modules.commentary.daily_matches import (
    process_daily_matches,
    clear_daily_commentaries_table,
    search_commentaries_by_date
)


def main():
    """Ana program"""
    
    parser = argparse.ArgumentParser(
        description='Günlük maçları işleyip veritabanına kaydet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python save_daily_matches.py 05/11/25                    # Maçları kaydet
  python save_daily_matches.py 05/11/25 --clear            # Önce tabloyu temizle
  python save_daily_matches.py 05/11/25 --show             # Kaydedilenleri göster
  python save_daily_matches.py 05/11/25 --no-save          # Sadece test et
  python save_daily_matches.py 05/11/25 --clear --no-save  # Temizle ve test et
        """
    )
    
    parser.add_argument(
        'match_date',
        help='Maç tarihi (format: DD/MM/YY, örn: 05/11/25)'
    )
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='İşlemden ÖNCE daily_match_commentaries tablosunu tamamen temizle'
    )
    
    parser.add_argument(
        '--show',
        action='store_true',
        help='İşlem sonrası kaydedilen maçları göster'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Veritabanına kaydetme, sadece test et (dry run)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("💾 GÜNLÜK MAÇLARI VERİTABANINA KAYDET")
    print("=" * 80)
    print(f"📅 Tarih: {args.match_date}")
    print(f"⏰ İşlem Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Veritabanı bağlantıları
    print("\n🔌 Veritabanı bağlantıları kuruluyor...")
    analytics_db = AnalyticsConnection()
    source_db = SourceConnection()
    print("✅ Bağlantılar başarılı!")
    
    # Tablo temizleme (opsiyonel)
    if args.clear:
        print("\n🗑️  Tablo temizleniyor...")
        if clear_daily_commentaries_table(analytics_db):
            print("✅ Tablo başarıyla temizlendi!")
        else:
            print("❌ Tablo temizleme başarısız!")
            return 1
    
    # Kaydetme durumunu belirt
    if args.no_save:
        print("\n🧪 TEST MODU: Maçlar işlenecek ama VERİTABANINA KAYDEDİLMEYECEK!")
        save_to_db = False
    else:
        print("\n💾 Maçlar işlenip VERİTABANINA KAYDEDİLECEK...")
        save_to_db = True
    
    print("\n" + "=" * 80)
    
    # Maçları işle
    try:
        commentaries = process_daily_matches(
            source_db=source_db,
            analytics_db=analytics_db,
            match_date=args.match_date,
            table_name='team_sum_last_10',
            save_to_db=save_to_db
        )
        
        if not commentaries:
            print(f"\n❌ {args.match_date} tarihinde işlenecek maç bulunamadı!")
            return 1
        
        print(f"\n✅ BAŞARILI! {len(commentaries)} maç işlendi.")
        
        # Kaydedilenleri göster (opsiyonel)
        if args.show and save_to_db:
            print("\n" + "=" * 80)
            print("📋 KAYDEDİLEN MAÇLAR")
            print("=" * 80)
            
            saved_matches = search_commentaries_by_date(analytics_db, args.match_date)
            
            if saved_matches is not None and len(saved_matches) > 0:
                print(f"\n✅ Toplam {len(saved_matches)} maç kaydı bulundu:\n")
                
                for idx, row in saved_matches.iterrows():
                    json_size = len(str(row['commentary_json']))
                    print(f"{idx + 1}. {row['home_team_name']} vs {row['away_team_name']}")
                    print(f"   🏆 {row['country']} - {row['league']}")
                    print(f"   ⏰ {row['match_time']}")
                    print(f"   📊 JSON Boyutu: {json_size:,} karakter")
                    print(f"   🆔 Match ID: {row['match_id']}")
                    print()
            else:
                print("❌ Kaydedilmiş maç bulunamadı!")
        
        print("\n" + "=" * 80)
        print("✅ İŞLEM TAMAMLANDI!")
        print("=" * 80)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  İşlem kullanıcı tarafından iptal edildi!")
        return 130
        
    except Exception as e:
        print(f"\n❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
