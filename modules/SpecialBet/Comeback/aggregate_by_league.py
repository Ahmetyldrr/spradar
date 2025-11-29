"""
AGGREGATE BY LEAGUE - Lig/Sezon Bazında Comeback Yorumlarını Birleştir

Bu script:
1. comprehensive_comeback_analysis tablosundan yorumları alır
2. season_id'ye göre gruplar
3. Tüm maçları tek bir JSON array içinde toplar
4. league_comeback_summary tablosuna kaydeder
"""

import sys
import os
import json
from datetime import datetime

# Projenin root dizinini ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from database.analytics_connection import AnalyticsConnection
from database.source_connection import SourceConnection
import pandas as pd


def create_league_summary_table():
    """
    league_comeback_summary tablosunu oluştur
    
    Tablo Yapısı:
    - season_id: INTEGER (PK)
    - season_name: TEXT (örn: "2024/2025")
    - league_name: TEXT (örn: "Premier League")
    - league_id: INTEGER
    - match_count: INTEGER (kaç maç var)
    - matches_json: JSONB (tüm maçların yorumları)
    - created_at: TIMESTAMP
    """
    
    analytics = AnalyticsConnection()
    
    create_sql = """
    CREATE TABLE IF NOT EXISTS league_comeback_summary (
        season_id INTEGER PRIMARY KEY,
        season_name TEXT,
        league_name TEXT,
        league_id INTEGER,
        match_count INTEGER,
        matches_json JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Index ekle
    CREATE INDEX IF NOT EXISTS idx_league_comeback_league_id ON league_comeback_summary(league_id);
    CREATE INDEX IF NOT EXISTS idx_league_comeback_season_name ON league_comeback_summary(season_name);
    """
    
    success = analytics.execute_query(create_sql)
    
    if success:
        print("✅ league_comeback_summary tablosu hazır!")
    else:
        print("❌ Tablo oluşturulamadı!")
        
    return success


def get_season_info_from_matches(season_id, match_df):
    """
    comprehensive_comeback_analysis tablosundan season bilgilerini al
    match_df içindeki ilk maçtan league_name bilgisini çıkar
    
    Returns:
        dict: {'season_name': str(season_id), 'league_name': 'Unknown', 'league_id': 0}
    """
    
    # İlk maçtan league_name çıkarmaya çalış (commentary_json içinden)
    if len(match_df) > 0:
        first_row = match_df.iloc[0]
        
        # commentary_json varsa parse et
        if pd.notnull(first_row.get('commentary_json')):
            try:
                commentary = first_row['commentary_json']
                if isinstance(commentary, str):
                    commentary = json.loads(commentary)
                
                # metadata içinden league_name al
                metadata = commentary.get('metadata', {})
                league_name = metadata.get('league_name', 'Unknown League')
                
            except:
                league_name = 'Unknown League'
        else:
            league_name = 'Unknown League'
    else:
        league_name = 'Unknown League'
    
    return {
        'season_id': season_id,
        'season_name': f'Season {season_id}',
        'league_name': league_name,
        'league_id': 0  # Bilinmiyor
    }


def aggregate_by_season():
    """
    comprehensive_comeback_analysis tablosundan verileri al
    season_id bazında grupla ve JSON olarak birleştir
    """
    
    print("\n" + "="*80)
    print("🏆 LİG BAZINDA COMEBACK YORUMLARI BİRLEŞTİRME")
    print("="*80 + "\n")
    
    analytics = AnalyticsConnection()
    
    # Mevcut yorumları al
    sql = """
    SELECT 
        season_id,
        match_id,
        home_team_id,
        home_team_name,
        away_team_id,
        away_team_name,
        match_date,
        home_comeback_score,
        away_comeback_score,
        combined_comeback_score,
        data_quality,
        commentary_json
    FROM 
        comprehensive_comeback_analysis
    ORDER BY 
        season_id, combined_comeback_score DESC
    """
    
    df = analytics.query_df(sql)
    
    if df is None or len(df) == 0:
        print("❌ Hiç veri bulunamadı!")
        return False
    
    print(f"📊 Toplam {len(df):,} maç yorumu bulundu")
    print(f"📋 Sezon sayısı: {df['season_id'].nunique()}\n")
    
    # season_id'ye göre grupla
    grouped = df.groupby('season_id')
    
    summary_data = []
    
    for season_id, group_df in grouped:
        print(f"\n{'='*60}")
        print(f"🔄 Season ID: {season_id} işleniyor...")
        print(f"{'='*60}")
        
        # Sezon bilgilerini al (match verilerinden)
        season_info = get_season_info_from_matches(season_id, group_df)
        
        if not season_info:
            print(f"⚠️ Season ID {season_id} için bilgi bulunamadı, atlanıyor...")
            continue
        
        print(f"📌 Sezon: {season_info['season_name']}")
        print(f"⚽ Lig: {season_info['league_name']}")
        print(f"🎯 Maç Sayısı: {len(group_df)}")
        
        # Tüm maçları JSON array'e dönüştür
        matches_list = []
        
        for idx, row in group_df.iterrows():
            match_data = {
                'match_id': int(row['match_id']),
                'home_team': {
                    'team_id': int(row['home_team_id']),
                    'team_name': row['home_team_name'],
                    'comeback_score': float(row['home_comeback_score'])
                },
                'away_team': {
                    'team_id': int(row['away_team_id']),
                    'team_name': row['away_team_name'],
                    'comeback_score': float(row['away_comeback_score'])
                },
                'match_date': str(row['match_date']) if pd.notnull(row['match_date']) else None,
                'combined_comeback_score': float(row['combined_comeback_score']),
                'data_quality': row['data_quality'],
                'commentary': row['commentary_json']  # Tam yorum (JSON)
            }
            
            matches_list.append(match_data)
        
        # Özet verisi oluştur
        summary_record = {
            'season_id': int(season_id),
            'season_name': season_info['season_name'],
            'league_name': season_info['league_name'],
            'league_id': int(season_info['league_id']),
            'match_count': len(group_df),
            'matches_json': json.dumps(matches_list, ensure_ascii=False)  # JSON string
        }
        
        summary_data.append(summary_record)
        
        # İlk 3 maçı göster
        top_3 = group_df.nlargest(3, 'combined_comeback_score')
        print(f"\n📈 En yüksek skorlu 3 maç:")
        for i, (_, match) in enumerate(top_3.iterrows(), 1):
            print(f"   {i}. {match['home_team_name']} vs {match['away_team_name']} - Skor: {match['combined_comeback_score']:.1f}")
    
    if not summary_data:
        print("\n❌ Hiç özet verisi oluşturulamadı!")
        return False
    
    # DataFrame'e çevir
    summary_df = pd.DataFrame(summary_data)
    
    print("\n" + "="*80)
    print("💾 VERİTABANINA KAYIT")
    print("="*80 + "\n")
    
    # Veritabanına kaydet
    insert_sql = """
    INSERT INTO league_comeback_summary 
        (season_id, season_name, league_name, league_id, match_count, matches_json, created_at)
    VALUES 
        (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (season_id) 
    DO UPDATE SET
        season_name = EXCLUDED.season_name,
        league_name = EXCLUDED.league_name,
        league_id = EXCLUDED.league_id,
        match_count = EXCLUDED.match_count,
        matches_json = EXCLUDED.matches_json,
        created_at = EXCLUDED.created_at
    """
    
    conn = analytics.connect()
    cursor = conn.cursor()
    
    for _, row in summary_df.iterrows():
        cursor.execute(insert_sql, (
            row['season_id'],
            row['season_name'],
            row['league_name'],
            row['league_id'],
            row['match_count'],
            row['matches_json'],
            datetime.now()
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ {len(summary_df)} sezon verisi league_comeback_summary tablosuna kaydedildi!\n")
    
    # Özet istatistikler
    print("="*80)
    print("📊 ÖZET İSTATİSTİKLER")
    print("="*80 + "\n")
    
    print(f"🏆 Toplam Sezon: {len(summary_df)}")
    print(f"⚽ Toplam Maç: {summary_df['match_count'].sum():,}")
    print(f"📈 Ortalama Maç/Sezon: {summary_df['match_count'].mean():.1f}")
    print(f"🎯 En fazla maç: {summary_df['match_count'].max()} ({summary_df.loc[summary_df['match_count'].idxmax(), 'league_name']})")
    print(f"📉 En az maç: {summary_df['match_count'].min()} ({summary_df.loc[summary_df['match_count'].idxmin(), 'league_name']})")
    
    print("\n" + "="*80)
    print("✅ İŞLEM TAMAMLANDI!")
    print("="*80 + "\n")
    
    # Örnek kullanım göster
    print("💡 VERİYE ERİŞİM ÖRNEĞİ:")
    print("-" * 60)
    print("""
-- Tüm ligleri listele
SELECT season_id, league_name, season_name, match_count 
FROM league_comeback_summary 
ORDER BY match_count DESC;

-- Belirli bir ligin tüm maç yorumlarını al
SELECT matches_json 
FROM league_comeback_summary 
WHERE league_name = 'Premier League';

-- JSON içindeki maçları sorgula
SELECT 
    season_name,
    league_name,
    jsonb_array_length(matches_json) as match_count,
    matches_json->0->>'match_id' as first_match_id
FROM league_comeback_summary;
    """)
    
    return True


def main():
    """Ana fonksiyon"""
    
    print("\n🚀 Comeback Yorumları Lig Bazında Birleştirme Başlıyor...\n")
    
    # 1. Tablo oluştur
    if not create_league_summary_table():
        print("❌ Tablo oluşturulamadı, çıkılıyor...")
        return
    
    print()
    
    # 2. Verileri grupla ve kaydet
    if not aggregate_by_season():
        print("❌ Veri birleştirme başarısız!")
        return
    
    print("\n🎉 Tüm işlemler başarıyla tamamlandı!")


if __name__ == "__main__":
    main()
