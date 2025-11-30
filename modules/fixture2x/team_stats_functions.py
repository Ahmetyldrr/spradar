"""
TEAM STATS FUNCTIONS - Takım İstatistiklerini Toplama
=====================================================
Team bazlı istatistik hesaplama fonksiyonları
"""

import pandas as pd
import numpy as np


def calculate_last_n_matches_stats(df, n_matches=5):
    """Son N maç istatistikleri hesapla"""
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    # Team ID'ye göre gruplama ve tarih sıralaması
    stats_list = []
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # Tarihe göre sırala (en yeni en üstte)
        team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # İstatistikleri hesapla
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'matches_played': len(last_n),
                'wins': len(last_n[last_n['result'] == 'GALİBİYET']),
                'draws': len(last_n[last_n['result'] == 'BERABERLİK']),
                'losses': len(last_n[last_n['result'] == 'MAĞLUBİYET']),
                'goals_for': last_n['team_score'].sum(),
                'goals_against': last_n['opponent_score'].sum(),
                'goal_difference': last_n['goal_difference'].sum(),
                'clean_sheets': last_n['clean_sheet'].sum(),
                'goals_conceded_zero': len(last_n[last_n['opponent_score'] == 0]),
                'total_goals_avg': last_n['total_goals'].mean(),
                'home_matches': len(last_n[last_n['is_home'] == 1]),
                'away_matches': len(last_n[last_n['is_away'] == 1])
            }
            
            # Yüzde hesaplamaları
            if stats['matches_played'] > 0:
                stats['win_percentage'] = (stats['wins'] / stats['matches_played']) * 100
                stats['draw_percentage'] = (stats['draws'] / stats['matches_played']) * 100
                stats['loss_percentage'] = (stats['losses'] / stats['matches_played']) * 100
            else:
                stats['win_percentage'] = 0
                stats['draw_percentage'] = 0  
                stats['loss_percentage'] = 0
                
            stats_list.append(stats)
    
    # DataFrame oluştur
    stats_df = pd.DataFrame(stats_list)
    return stats_df


def calculate_sum_all_stats(df, n_matches=5):
    """TÜM İSTATİSTİKLERİ TOPLA - Her kolon için SUM!"""
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    stats_list = []
    
    # Toplanabilir kolonları bul (sayısal olanlar)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # AKILLI EXCLUDE SİSTEMİ!
    exclude_cols = []
    
    # 1️⃣ Gereksiz ID'ler - tamamen çıkar
    remove_ids = ['match_id', 'fixture_id', 'opponent_team_id', 'timestamp', 'unix']
    for col in numeric_cols:
        if any(x in col.lower() for x in remove_ids):
            exclude_cols.append(col)
    
    # 2️⃣ Sabit değerler - toplanmaz ama kalır (her satırda aynı değer)
    constant_cols = ['season_id', 'team_id', 'tournament_id', 'country_id']
    for col in constant_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    # 3️⃣ Teknik alanlar - toplanmaz
    technical_cols = ['week', 'stadiumid', 'round']
    for col in technical_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    print(f"   📊 Toplam sayısal kolon: {len(numeric_cols)}")
    print(f"   🗑️ Exclude edilen: {exclude_cols}")
    print(f"   🔥 Toplanacak: {len(numeric_cols) - len(exclude_cols)} kolon")
    
    # NE VARSA TOPLA! (ID'ler hariç)
    sum_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # Tarihe göre sırala (en yeni en üstte)
        team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler + önemli text bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n)
            }
            
            # Sabit değerleri ekle (toplanmaz ama önemli bilgi)
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]  # İlk değeri al (hepsi aynı)
            
            # TÜM SAYISAL KOLONLARI OTOMATİK TOPLA!
            for col in sum_cols:
                if col in last_n.columns:
                    # NULL değerleri 0 ile değiştir
                    col_data = last_n[col].fillna(0)
                    
                    # Sum ekle (NULL-safe)
                    stats[f'sum_{col}'] = col_data.sum()
                    # Ortalama da ekle (NULL-safe)
                    stats[f'avg_{col}'] = round(col_data.mean(), 2)
            
            stats_list.append(stats)
    
    # Final DataFrame'i de NULL-safe yap
    result_df = pd.DataFrame(stats_list)
    
    # Tüm sayısal kolonlardaki NULL'ları 0 ile değiştir
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df


def calculate_sum_home_stats(df, n_matches=5):
    """SADECE EV SAHİBİ MAÇLARI - TÜM İSTATİSTİKLERİ TOPLA"""
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    # SADECE EV SAHİBİ MAÇLARI FİLTRELE!
    df = df[df['is_home'] == 1].copy()
    print(f"   🏠 Ev sahibi maçları filtresi uygulandı: {len(df)} kayıt")
    
    stats_list = []
    
    # Toplanabilir kolonları bul (sayısal olanlar)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # AKILLI EXCLUDE SİSTEMİ!
    exclude_cols = []
    
    # 1️⃣ Gereksiz ID'ler - tamamen çıkar
    remove_ids = ['match_id', 'fixture_id', 'opponent_team_id', 'timestamp', 'unix']
    for col in numeric_cols:
        if any(x in col.lower() for x in remove_ids):
            exclude_cols.append(col)
    
    # 2️⃣ Sabit değerler - toplanmaz ama kalır (her satırda aynı değer)
    constant_cols = ['season_id', 'team_id', 'tournament_id', 'country_id', 'is_home', 'is_away']
    for col in constant_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    # 3️⃣ Teknik alanlar - toplanmaz
    technical_cols = ['week', 'stadiumid', 'round']
    for col in technical_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    print(f"   📊 Toplam sayısal kolon: {len(numeric_cols)}")
    print(f"   🗑️ Exclude edilen: {exclude_cols}")
    print(f"   🔥 Toplanacak: {len(numeric_cols) - len(exclude_cols)} kolon")
    
    # NE VARSA TOPLA! (ID'ler hariç)
    sum_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # Tarihe göre sırala (en yeni en üstte)
        team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler + önemli text bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n),
                'match_type': 'HOME'  # �� Ev sahibi maçları
            }
            
            # Sabit değerleri ekle (toplanmaz ama önemli bilgi)
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]  # İlk değeri al (hepsi aynı)
            
            # TÜM SAYISAL KOLONLARI OTOMATİK TOPLA!
            for col in sum_cols:
                if col in last_n.columns:
                    # NULL değerleri 0 ile değiştir
                    col_data = last_n[col].fillna(0)
                    
                    # Sum ekle (NULL-safe)
                    stats[f'sum_{col}'] = col_data.sum()
                    # Ortalama da ekle (NULL-safe)
                    stats[f'avg_{col}'] = round(col_data.mean(), 2)
            
            stats_list.append(stats)
    
    # Final DataFrame'i de NULL-safe yap
    result_df = pd.DataFrame(stats_list)
    
    # Tüm sayısal kolonlardaki NULL'ları 0 ile değiştir
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df


def calculate_sum_away_stats(df, n_matches=5):
    """SADECE DEPLASMAN MAÇLARI - TÜM İSTATİSTİKLERİ TOPLA"""
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    # SADECE DEPLASMAN MAÇLARI FİLTRELE!
    df = df[df['is_away'] == 1].copy()
    print(f"   ✈️ Deplasman maçları filtresi uygulandı: {len(df)} kayıt")
    
    stats_list = []
    
    # Toplanabilir kolonları bul (sayısal olanlar)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # AKILLI EXCLUDE SİSTEMİ!
    exclude_cols = []
    
    # 1️⃣ Gereksiz ID'ler - tamamen çıkar
    remove_ids = ['match_id', 'fixture_id', 'opponent_team_id', 'timestamp', 'unix']
    for col in numeric_cols:
        if any(x in col.lower() for x in remove_ids):
            exclude_cols.append(col)
    
    # 2️⃣ Sabit değerler - toplanmaz ama kalır (her satırda aynı değer)
    constant_cols = ['season_id', 'team_id', 'tournament_id', 'country_id', 'is_home', 'is_away']
    for col in constant_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    # 3️⃣ Teknik alanlar - toplanmaz
    technical_cols = ['week', 'stadiumid', 'round']
    for col in technical_cols:
        if col in numeric_cols:
            exclude_cols.append(col)
    
    print(f"   📊 Toplam sayısal kolon: {len(numeric_cols)}")
    print(f"   🗑️ Exclude edilen: {exclude_cols}")
    print(f"   🔥 Toplanacak: {len(numeric_cols) - len(exclude_cols)} kolon")
    
    # NE VARSA TOPLA! (ID'ler hariç)
    sum_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # Tarihe göre sırala (en yeni en üstte)
        team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler + önemli text bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n),
                'match_type': 'AWAY'  # ✈️ Deplasman maçları
            }
            
            # Sabit değerleri ekle (toplanmaz ama önemli bilgi)
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]  # İlk değeri al (hepsi aynı)
            
            # TÜM SAYISAL KOLONLARI OTOMATİK TOPLA!
            for col in sum_cols:
                if col in last_n.columns:
                    # NULL değerleri 0 ile değiştir
                    col_data = last_n[col].fillna(0)
                    
                    # Sum ekle (NULL-safe)
                    stats[f'sum_{col}'] = col_data.sum()
                    # Ortalama da ekle (NULL-safe)
                    stats[f'avg_{col}'] = round(col_data.mean(), 2)
            
            stats_list.append(stats)
    
    # Final DataFrame'i de NULL-safe yap
    result_df = pd.DataFrame(stats_list)
    
    # Tüm sayısal kolonlardaki NULL'ları 0 ile değiştir
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df


def calculate_dynamic_streaks(df, n_matches=5):
    """
    🔥 DİNAMİK STREAK HESAPLAMASI - Her özellik için streak!
    =====================================================
    
    Bu fonksiyon tüm sayısal özellikleri otomatik tespit eder ve
    her özellik için streak hesaplar (ardışık aynı durum).
    
    Örnek streak'ler:
    - win_streak: Ardışık galibiyetler
    - goals_streak: Ardışık gol atan maçlar 
    - clean_sheet_streak: Ardışık temiz çarşaf
    - positive_result_streak: Ardışık pozitif sonuçlar
    """
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    stats_list = []
    
    # Streak hesaplanabilir özellikleri bul
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Streak için uygun olmayan kolonları filtrele
    exclude_cols = []
    
    # 1️⃣ ID'ler ve teknik alanlar
    remove_patterns = ['match_id', 'fixture_id', 'team_id', 'opponent_team_id', 
                       'season_id', 'tournament_id', 'country_id', 'timestamp',
                       'unix', 'week', 'stadiumid', 'round']
    
    for col in numeric_cols:
        if any(pattern in col.lower() for pattern in remove_patterns):
            exclude_cols.append(col)
    
    # Streak hesaplanacak kolonlar
    streak_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    print(f"   🔥 Streak hesaplanacak özellikler: {len(streak_cols)} adet")
    print(f"   📋 Özellikler: {streak_cols[:10]}..." if len(streak_cols) > 10 else f"   📋 Özellikler: {streak_cols}")
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # HAFTA (ROUND) NUMARASINA GÖRE SIRALA (en yeni hafta en üstte)
        if 'round' in team_matches.columns:
            team_matches = team_matches.sort_values('round', ascending=False)
        else:
            # Fallback: Tarihe göre sırala
            team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n),
                'analysis_type': 'DYNAMIC_STREAKS'
            }
            
            # Sabit değerleri ekle
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]
            
            # 🔥 DİNAMİK STREAK HESAPLAMASI!
            for col in streak_cols:
                if col in last_n.columns:
                    # En yeni maçtan başlayarak streak hesapla (round ile sıralandı)
                    data = last_n[col].fillna(0)
                    
                    # AKILLI BİNARY ÇEVİRİM + ROUND İLE GÜVENLİ!
                    # Eğer kolon zaten binary değilse (0/1), binary'e çevir
                    unique_vals = set(data.unique())
                    if unique_vals <= {0, 1, 0.0, 1.0}:
                        # Zaten binary, round ile güvenli çevir
                        binary_data = data.round().astype(int)
                    else:
                        # Binary değil, pozitif değerleri 1 yap
                        binary_data = (data > 0).astype(int)
                    
                    # BİNARY STREAK HESAPLA (1 değerlerinin ardışık sayısı)
                    current_streak = 0
                    for value in binary_data:
                        if value == 1:  # Sadece 1 değerleri için streak
                            current_streak += 1
                        else:
                            break
                    
                    # Tek streak değeri ekle
                    stats[f'streak_{col}'] = current_streak
            
            stats_list.append(stats)
    
    # Final DataFrame
    result_df = pd.DataFrame(stats_list)
    
    # NULL değerleri temizle
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df


def calculate_dynamic_streaks_home(df, n_matches=5):
    """
    🏠 DİNAMİK STREAK HESAPLAMASI - SADECE EV SAHİBİ MAÇLARI!
    ========================================================
    
    Sadece ev sahibi maçları için her özellik bazında streak hesaplar.
    """
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    # SADECE EV SAHİBİ MAÇLARI FİLTRELE!
    df = df[df['is_home'] == 1].copy()
    print(f"   🏠 Ev sahibi maçları filtresi uygulandı: {len(df)} kayıt")
    
    stats_list = []
    
    # Streak hesaplanabilir özellikleri bul
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Streak için uygun olmayan kolonları filtrele
    exclude_cols = []
    
    # ID'ler ve teknik alanlar
    remove_patterns = ['match_id', 'fixture_id', 'team_id', 'opponent_team_id', 
                       'season_id', 'tournament_id', 'country_id', 'timestamp',
                       'unix', 'week', 'stadiumid', 'round', 'is_home', 'is_away']
    
    for col in numeric_cols:
        if any(pattern in col.lower() for pattern in remove_patterns):
            exclude_cols.append(col)
    
    # Streak hesaplanacak kolonlar
    streak_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    print(f"   🔥 Ev sahibi streak özellikleri: {len(streak_cols)} adet")
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # HAFTA (ROUND) NUMARASINA GÖRE SIRALA (en yeni hafta en üstte)
        if 'round' in team_matches.columns:
            team_matches = team_matches.sort_values('round', ascending=False)
        else:
            # Fallback: Tarihe göre sırala
            team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n),
                'analysis_type': 'HOME_STREAKS'
            }
            
            # Sabit değerleri ekle
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]
            
            # 🏠 EV SAHİBİ STREAK HESAPLAMASI!
            for col in streak_cols:
                if col in last_n.columns:
                    # En yeni maçtan başlayarak streak hesapla (round ile sıralandı)
                    data = last_n[col].fillna(0)
                    
                    # AKILLI BİNARY ÇEVİRİM + ROUND İLE GÜVENLİ!
                    # Eğer kolon zaten binary değilse (0/1), binary'e çevir
                    unique_vals = set(data.unique())
                    if unique_vals <= {0, 1, 0.0, 1.0}:
                        # Zaten binary, round ile güvenli çevir
                        binary_data = data.round().astype(int)
                    else:
                        # Binary değil, pozitif değerleri 1 yap
                        binary_data = (data > 0).astype(int)
                    
                    # BİNARY STREAK HESAPLA (1 değerlerinin ardışık sayısı)
                    current_streak = 0
                    for value in binary_data:
                        if value == 1:  # Sadece 1 değerleri için streak
                            current_streak += 1
                        else:
                            break
                    
                    # Tek streak değeri ekle
                    stats[f'streak_{col}'] = current_streak
            
            stats_list.append(stats)
    
    # Final DataFrame
    result_df = pd.DataFrame(stats_list)
    
    # NULL değerleri temizle
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df


def calculate_dynamic_streaks_away(df, n_matches=5):
    """
    ✈️ DİNAMİK STREAK HESAPLAMASI - SADECE DEPLASMAN MAÇLARI!
    =========================================================
    
    Sadece deplasman maçları için her özellik bazında streak hesaplar.
    """
    df = df.copy()
    
    # Tarih sütununu datetime'a çevir
    if 'match_date' in df.columns:
        df['match_date'] = pd.to_datetime(df['match_date'], format='%d/%m/%y', errors='coerce')
    
    # SADECE DEPLASMAN MAÇLARI FİLTRELE!
    df = df[df['is_away'] == 1].copy()
    print(f"   ✈️ Deplasman maçları filtresi uygulandı: {len(df)} kayıt")
    
    stats_list = []
    
    # Streak hesaplanabilir özellikleri bul
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Streak için uygun olmayan kolonları filtrele
    exclude_cols = []
    
    # ID'ler ve teknik alanlar
    remove_patterns = ['match_id', 'fixture_id', 'team_id', 'opponent_team_id', 
                       'season_id', 'tournament_id', 'country_id', 'timestamp',
                       'unix', 'week', 'stadiumid', 'round', 'is_home', 'is_away']
    
    for col in numeric_cols:
        if any(pattern in col.lower() for pattern in remove_patterns):
            exclude_cols.append(col)
    
    # Streak hesaplanacak kolonlar
    streak_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    print(f"   🔥 Deplasman streak özellikleri: {len(streak_cols)} adet")
    
    for team_id in df['team_id'].unique():
        team_matches = df[df['team_id'] == team_id].copy()
        
        # HAFTA (ROUND) NUMARASINA GÖRE SIRALA (en yeni hafta en üstte)
        if 'round' in team_matches.columns:
            team_matches = team_matches.sort_values('round', ascending=False)
        else:
            # Fallback: Tarihe göre sırala
            team_matches = team_matches.sort_values('match_date', ascending=False)
        
        # Son N maçı al
        last_n = team_matches.head(n_matches)
        
        if len(last_n) > 0:
            # Temel bilgiler
            stats = {
                'team_id': team_id,
                'team_name': last_n['team_name'].iloc[0],
                'country_name': last_n['country_name'].iloc[0] if 'country_name' in last_n.columns else None,
                'tournament_name': last_n['tournament_name'].iloc[0] if 'tournament_name' in last_n.columns else None,
                'matches_played': len(last_n),
                'analysis_type': 'AWAY_STREAKS'
            }
            
            # Sabit değerleri ekle
            constant_cols = ['season_id', 'tournament_id', 'country_id']
            for col in constant_cols:
                if col in last_n.columns:
                    stats[col] = last_n[col].iloc[0]
            
            # ✈️ DEPLASMAN STREAK HESAPLAMASI!
            for col in streak_cols:
                if col in last_n.columns:
                    # En yeni maçtan başlayarak streak hesapla (round ile sıralandı)
                    data = last_n[col].fillna(0)
                    
                    # AKILLI BİNARY ÇEVİRİM + ROUND İLE GÜVENLİ!
                    # Eğer kolon zaten binary değilse (0/1), binary'e çevir
                    unique_vals = set(data.unique())
                    if unique_vals <= {0, 1, 0.0, 1.0}:
                        # Zaten binary, round ile güvenli çevir
                        binary_data = data.round().astype(int)
                    else:
                        # Binary değil, pozitif değerleri 1 yap
                        binary_data = (data > 0).astype(int)
                    
                    # BİNARY STREAK HESAPLA (1 değerlerinin ardışık sayısı)
                    current_streak = 0
                    for value in binary_data:
                        if value == 1:  # Sadece 1 değerleri için streak
                            current_streak += 1
                        else:
                            break
                    
                    # Tek streak değeri ekle
                    stats[f'streak_{col}'] = current_streak
            
            stats_list.append(stats)
    
    # Final DataFrame
    result_df = pd.DataFrame(stats_list)
    
    # NULL değerleri temizle
    numeric_columns = result_df.select_dtypes(include=[np.number]).columns
    result_df[numeric_columns] = result_df[numeric_columns].fillna(0)
    
    return result_df
