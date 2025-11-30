"""
🎯 DAILY MATCH COMMENTARY GENERATOR
===================================

Günlük maçları otomatik analiz eden ve yorum oluşturan sistem.

Özellikler:
- current_week_fixtures tablosundan günün maçlarını çeker
- Her maç için otomatik takım yorumu oluşturur
- Maç bilgileri + yorumları JSON formatında saklar
- Toplu işlem yapabilir

Author: Spradar Analytics Team
Date: November 5, 2025
Version: 2.0
"""

import json
from datetime import datetime
import pandas as pd


def get_daily_matches(source_db, match_date=None):
    """
    📅 GÜNLÜK MAÇLARI ÇEK
    ====================
    
    current_week_fixtures tablosundan belirli bir günün maçlarını çeker.
    
    Args:
        source_db: Source veritabanı bağlantısı
        match_date (str): Maç tarihi (format: DD/MM/YY) - None ise bugün
        
    Returns:
        DataFrame: Günün maçları
    """
    
    if match_date is None:
        # Bugünün tarihi
        match_date = datetime.now().strftime('%d/%m/%y')
    
    query = """
    SELECT 
        country_name,
        tournament_name,
        season_id,
        match_id,
        round,
        week,
        status,
        roundname,
        comment,
        neutralground,
        stadiumid,
        created_date,
        match_date,
        match_time,
        timezone,
        unix_timestamp,
        home_team_id,
        home_team_name,
        away_team_id,
        away_team_name,
        home_score_1h,
        away_score_1h,
        home_score,
        away_score,
        result_period,
        winner,
        postponed
    FROM public.current_week_fixtures
    WHERE match_date = %s
    ORDER BY unix_timestamp, match_time
    """
    
    df = source_db.query_df(query, params=(match_date,))
    
    return df


def generate_match_commentary_with_info(analytics_db, source_db, home_team_id, away_team_id, 
                                       match_info, table_name='team_sum_last_10'):
    """
    🏟️ MAÇ YORUMU + BİLGİLERİ OLUŞTUR
    ==================================
    
    Maç bilgileri + iki takımın yorumlarını birleştirip JSON oluşturur.
    commetar.py mantığı ile takım isimlerini çıkarır.
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        source_db: Source veritabanı bağlantısı
        home_team_id (int): Ev sahibi takım ID
        away_team_id (int): Deplasman takımı ID
        match_info (dict): Maç bilgileri (home_team_name, away_team_name içermeli)
        table_name (str): Analiz tablosu adı
        
    Returns:
        dict: Maç yorumu JSON
    """
    
    from modules.commentary.comprehensive_commentary import generate_comprehensive_natural_commentary
    
    # İki takımın veri satırlarını çek - sum_all_match_played dahil
    home_query = f"SELECT * FROM {table_name} WHERE team_id = %s"
    away_query = f"SELECT * FROM {table_name} WHERE team_id = %s"
    
    home_df = analytics_db.query_df(home_query, params=(home_team_id,))
    away_df = analytics_db.query_df(away_query, params=(away_team_id,))
    
    # Oynadıkları maç sayısını al
    home_matches_played = 0
    away_matches_played = 0
    
    if home_df is None or len(home_df) == 0:
        home_commentary = f"Ev sahibi takım (ID: {home_team_id}) için veri bulunamadı."
        home_team_name_fallback = f"Takım {home_team_id}"
    else:
        home_row = home_df.iloc[0].to_dict()
        home_commentary = generate_comprehensive_natural_commentary(home_row)
        home_team_name_fallback = home_row.get('team_name', f"Takım {home_team_id}")
        home_matches_played = int(home_row.get('sum_all_matches_played', 0) or 0)
    
    if away_df is None or len(away_df) == 0:
        away_commentary = f"Deplasman takımı (ID: {away_team_id}) için veri bulunamadı."
        away_team_name_fallback = f"Takım {away_team_id}"
    else:
        away_row = away_df.iloc[0].to_dict()
        away_commentary = generate_comprehensive_natural_commentary(away_row)
        away_team_name_fallback = away_row.get('team_name', f"Takım {away_team_id}")
        away_matches_played = int(away_row.get('sum_all_matches_played', 0) or 0)
    
    # Takım isimlerini çıkar (commetar.py mantığı)
    # Önce match_info'dan al, yoksa fallback kullan
    home_team_name = match_info.get('home_team_name', home_team_name_fallback)
    away_team_name = match_info.get('away_team_name', away_team_name_fallback)
    
    # BİRLEŞİK PROMPT OLUŞTUR (commetar.py mantığı - SADELEŞTİRİLMİŞ YAPI)
    # Maç temel bilgileri + Oynanmış maç sayıları
    base_info = f"""MAÇ BİLGİLERİ:
Lig: {match_info.get('country_name')} - {match_info.get('tournament_name')}
Tarih: {match_info.get('match_date')} {match_info.get('match_time')} ({match_info.get('timezone')})
Ev Sahibi: {home_team_name} (ID: {home_team_id}) - {home_matches_played} maç oynamış
Deplasman: {away_team_name} (ID: {away_team_id}) - {away_matches_played} maç oynamış
Hafta: {match_info.get('round')}
Sezon ID: {match_info.get('season_id')}

"""

    # Tam birleşik prompt
    combined_prompt = base_info + f"""EV SAHİBİ - {home_team_name.upper()}:
{home_commentary}

DEPLASMAN - {away_team_name.upper()}:
{away_commentary}"""

    # SADELEŞTİRİLMİŞ JSON YAPISI - SADECE combined_prompt!
    match_commentary_json = {
        "combined_prompt": combined_prompt,  # Ana prompt - Maç bilgileri + 2 takım + Sorular
        "metadata": {
            "match_id": match_info.get('match_id'),
            "match_date": match_info.get('match_date'),
            "match_time": match_info.get('match_time'),
            "home_team_id": home_team_id,
            "home_team_name": home_team_name,
            "home_matches_played": home_matches_played,
            "away_team_id": away_team_id,
            "away_team_name": away_team_name,
            "away_matches_played": away_matches_played,
            "country": match_info.get('country_name'),
            "league": match_info.get('tournament_name'),
            "season_id": match_info.get('season_id'),
            "round": match_info.get('round'),
            "generated_at": datetime.now().isoformat(),
            "system_version": "4.0",
            "data_source": "team_sum_last_10",
            "commentary_type": "comprehensive_286_columns",
            "format": "combined_prompt_only"
        }
    }
    
    return match_commentary_json


def process_daily_matches(source_db, analytics_db, match_date=None, 
                         table_name='team_sum_last_10', save_to_db=True):
    """
    🎯 GÜNLÜK MAÇLARI İŞLE
    ======================
    
    Belirli bir günün tüm maçlarını işleyip yorumları oluşturur.
    
    Args:
        source_db: Source veritabanı bağlantısı
        analytics_db: Analytics veritabanı bağlantısı
        match_date (str): Maç tarihi (None ise bugün)
        table_name (str): Analiz tablosu
        save_to_db (bool): Veritabanına kaydet
        
    Returns:
        list: Tüm maç yorumları
    """
    
    print(f"\n{'='*80}")
    print(f"🎯 GÜNLÜK MAÇ YORUM İŞLEME SİSTEMİ")
    print(f"{'='*80}")
    
    # Tarihi belirle
    if match_date is None:
        match_date = datetime.now().strftime('%d/%m/%y')
    
    print(f"\n📅 Tarih: {match_date}")
    
    # Günün maçlarını çek
    matches_df = get_daily_matches(source_db, match_date)
    
    if matches_df is None or len(matches_df) == 0:
        print(f"❌ {match_date} tarihinde maç bulunamadı!")
        return []
    
    print(f"✅ {len(matches_df)} maç bulundu!")
    print(f"\n{'='*80}")
    
    all_match_commentaries = []
    
    # Her maç için işlem yap
    for idx, row in matches_df.iterrows():
        match_num = idx + 1
        print(f"\n📊 Maç {match_num}/{len(matches_df)}: {row['home_team_name']} vs {row['away_team_name']}")
        print(f"   🏆 Lig: {row['country_name']} - {row['tournament_name']}")
        print(f"   ⏰ Saat: {row['match_time']} ({row['timezone']})")
        
        try:
            # Maç bilgilerini hazırla
            match_info = {
                'match_id': row['match_id'],
                'match_date': row['match_date'],
                'match_time': row['match_time'],
                'timezone': row['timezone'],
                'country_name': row['country_name'],
                'tournament_name': row['tournament_name'],
                'season_id': row['season_id'],
                'round': row['round'],
                'week': row['week'],
                'stadiumid': row['stadiumid'],
                'status': row['status'],
                'home_team_name': row['home_team_name'],
                'away_team_name': row['away_team_name']
            }
            
            # Yorum oluştur
            print(f"   🔄 Yorumlar oluşturuluyor...")
            match_commentary = generate_match_commentary_with_info(
                analytics_db,
                source_db,
                row['home_team_id'],
                row['away_team_id'],
                match_info,
                table_name
            )
            
            all_match_commentaries.append(match_commentary)
            
            print(f"   ✅ Başarılı!")
            
            # Veritabanına kaydet (opsiyonel)
            if save_to_db:
                save_commentary_to_db(analytics_db, match_commentary)
            
        except Exception as e:
            print(f"   ❌ Hata: {str(e)}")
            continue
    
    print(f"\n{'='*80}")
    print(f"✅ İŞLEM TAMAMLANDI!")
    print(f"📊 Toplam {len(all_match_commentaries)}/{len(matches_df)} maç başarıyla işlendi.")
    print(f"{'='*80}\n")
    
    return all_match_commentaries


def clear_daily_commentaries_table(analytics_db):
    """
    🗑️ GÜNLÜK YORUM TABLOSUNU TEMİZLE
    ==================================
    
    daily_match_commentaries tablosundaki TÜM kayıtları siler.
    Tablo yoksa önce oluşturur, sonra temizler.
    ⚠️ DİKKAT: Tablo yapısı korunur, sadece veriler silinir!
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        
    Returns:
        bool: Başarılı ise True
    """
    try:
        conn = analytics_db.connect()
        if not conn:
            print("❌ Veritabanı bağlantısı başarısız!")
            return False
        
        cursor = conn.cursor()
        
        # Önce tabloyu tamamen sil ve yeniden oluştur (yapı değiştiği için)
        cursor.execute("DROP TABLE IF EXISTS daily_match_commentaries CASCADE;")
        conn.commit()
        
        # Yeni yapıyla tabloyu oluştur
        create_table_query = """
        CREATE TABLE IF NOT EXISTS daily_match_commentaries (
            id SERIAL PRIMARY KEY,
            match_id BIGINT UNIQUE NOT NULL,
            match_date VARCHAR(10) NOT NULL,
            match_time VARCHAR(10),
            home_team_id BIGINT NOT NULL,
            away_team_id BIGINT NOT NULL,
            home_team_name VARCHAR(255) NOT NULL,
            away_team_name VARCHAR(255) NOT NULL,
            home_matches_played INTEGER DEFAULT 0,
            away_matches_played INTEGER DEFAULT 0,
            control_count VARCHAR(20) DEFAULT 'INCOMPLETE',
            league VARCHAR(255),
            country VARCHAR(255),
            commentary_json JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_daily_match_date ON daily_match_commentaries(match_date);
        CREATE INDEX IF NOT EXISTS idx_daily_match_id ON daily_match_commentaries(match_id);
        CREATE INDEX IF NOT EXISTS idx_control_count ON daily_match_commentaries(control_count);
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ daily_match_commentaries tablosu yeniden oluşturuldu!")
        return True
        
    except Exception as e:
        print(f"❌ Tablo temizleme hatası: {e}")
        if conn:
            conn.close()
        return False


def save_commentary_to_db(analytics_db, match_commentary):
    """
    💾 YORUMU VERİTABANINA KAYDET
    =============================
    
    Maç yorumunu analytics veritabanına JSON olarak kaydeder.
    ⚠️ UPSERT kullanır: Aynı match_id varsa günceller, yoksa ekler.
    ⚠️ CREATE TABLE IF NOT EXISTS: Tablo yoksa oluşturur, varsa DOKUNMAZ!
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        match_commentary (dict): Maç yorumu JSON
    """
    
    try:
        # Tablo yoksa oluştur (VARSA DOKUNMA!)
        conn = analytics_db.connect()
        if not conn:
            print("❌ Veritabanı bağlantısı başarısız!")
            return False
        
        cursor = conn.cursor()
        
        # IF NOT EXISTS = Tablo varsa hiçbir şey yapmaz!
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS daily_match_commentaries (
            id SERIAL PRIMARY KEY,
            match_id BIGINT UNIQUE,
            match_date VARCHAR(20),
            match_time VARCHAR(20),
            country TEXT,
            league TEXT,
            home_team_id INTEGER,
            home_team_name TEXT,
            away_team_id INTEGER,
            away_team_name TEXT,
            commentary_json JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_match_id ON daily_match_commentaries(match_id);
        CREATE INDEX IF NOT EXISTS idx_match_date ON daily_match_commentaries(match_date);
        CREATE INDEX IF NOT EXISTS idx_home_team ON daily_match_commentaries(home_team_id);
        CREATE INDEX IF NOT EXISTS idx_away_team ON daily_match_commentaries(away_team_id);
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        # Veriyi kaydet (UPSERT) - home_matches_played, away_matches_played ve control_count dahil
        insert_query = """
        INSERT INTO daily_match_commentaries (
            match_id, match_date, match_time, country, league,
            home_team_id, home_team_name, home_matches_played,
            away_team_id, away_team_name, away_matches_played,
            control_count, commentary_json
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (match_id) 
        DO UPDATE SET
            commentary_json = EXCLUDED.commentary_json,
            home_matches_played = EXCLUDED.home_matches_played,
            away_matches_played = EXCLUDED.away_matches_played,
            control_count = EXCLUDED.control_count,
            created_at = CURRENT_TIMESTAMP
        """
        
        # SADELEŞTİRİLMİŞ JSON YAPISI - metadata'dan al
        metadata = match_commentary['metadata']
        
        # Control count hesapla: Her iki takım da 10 maç oynadıysa OK, değilse INCOMPLETE
        home_matches = metadata.get('home_matches_played', 0)
        away_matches = metadata.get('away_matches_played', 0)
        control_count = 'OK' if (home_matches == 10 and away_matches == 10) else 'INCOMPLETE'
        
        params = (
            metadata['match_id'],
            metadata['match_date'],
            metadata['match_time'],
            metadata['country'],
            metadata['league'],
            metadata['home_team_id'],
            metadata['home_team_name'],
            home_matches,
            metadata['away_team_id'],
            metadata['away_team_name'],
            away_matches,
            control_count,
            json.dumps(match_commentary, ensure_ascii=False)
        )
        
        cursor.execute(insert_query, params)
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Veritabanı kaydetme hatası: {e}")
        if conn:
            conn.close()
        return False


def save_all_commentaries_to_file(commentaries, output_file=None):
    """
    💾 TÜM YORUMLARI DOSYAYA KAYDET
    ===============================
    
    Args:
        commentaries (list): Tüm maç yorumları
        output_file (str): Çıktı dosya adı
        
    Returns:
        str: Kaydedilen dosya adı
    """
    
    if output_file is None:
        output_file = f"daily_commentaries_{datetime.now().strftime('%Y%m%d')}.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(commentaries, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Tüm yorumlar '{output_file}' dosyasına kaydedildi!")
        return output_file
        
    except Exception as e:
        print(f"\n❌ Dosya kaydetme hatası: {e}")
        return None


def get_match_commentary_from_db(analytics_db, match_id):
    """
    📖 VERİTABANINDAN YORUM ÇEK
    ===========================
    
    Belirli bir maçın yorumunu veritabanından çeker.
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        match_id (int): Maç ID
        
    Returns:
        dict: Maç yorumu
    """
    
    query = """
    SELECT commentary_json
    FROM daily_match_commentaries
    WHERE match_id = %s
    """
    
    result = analytics_db.query_df(query, params=(match_id,))
    
    if result is not None and len(result) > 0:
        return result['commentary_json'].iloc[0]
    
    return None


def search_commentaries_by_date(analytics_db, match_date):
    """
    🔍 TARİHE GÖRE YORUM ARA
    ========================
    
    Belirli bir tarihteki tüm maç yorumlarını getirir.
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        match_date (str): Maç tarihi (DD/MM/YY)
        
    Returns:
        DataFrame: Maç yorumları
    """
    
    query = """
    SELECT 
        match_id,
        match_date,
        match_time,
        country,
        league,
        home_team_name,
        away_team_name,
        commentary_json,
        created_at
    FROM daily_match_commentaries
    WHERE match_date = %s
    ORDER BY match_time
    """
    
    return analytics_db.query_df(query, params=(match_date,))


def search_commentaries_by_team(analytics_db, team_id):
    """
    🔍 TAKIMA GÖRE YORUM ARA          
    ========================
    
    Belirli bir takımın maç yorumlarını getirir.
    
    Args:
        analytics_db: Analytics veritabanı bağlantısı
        team_id (int): Takım ID
        
    Returns:
        DataFrame: Takımın maç yorumları
    """
    
    query = """
    SELECT 
        match_id,
        match_date,
        match_time,
        country,
        league,
        home_team_name,
        away_team_name,
        commentary_json,
        created_at
    FROM daily_match_commentaries
    WHERE home_team_id = %s OR away_team_id = %s
    ORDER BY match_date DESC, match_time DESC
    """
    
    return analytics_db.query_df(query, params=(team_id, team_id))
