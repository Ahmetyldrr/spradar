"""
ÖRNEK FONKSİYONLAR - Kendi fonksiyonlarını buraya ekle
==================================================
"""

import pandas as pd
import numpy as np




def add_result(df):
    """ binary olarak Maç sonucunu ekle .astype(int) kullanbilirsin"""
    df = df.copy()

    df['ht_win'] = (df['team_score_1h'] > df['opponent_score_1h']).astype(int)
    df['ht_draw'] = (df['team_score_1h'] == df['opponent_score_1h']).astype(int)
    df['ht_loss'] = (df['team_score_1h'] < df['opponent_score_1h']).astype(int)

    df['ht2_win'] = (df['team_score_2h'] > df['opponent_score_2h']).astype(int)
    df['ht2_draw'] = (df['team_score_2h'] == df['opponent_score_2h']).astype(int)
    df['ht2_loss'] = (df['team_score_2h'] < df['opponent_score_2h']).astype(int)

    df['ft_win'] = (df['team_score'] > df['opponent_score']).astype(int)
    df['ft_draw'] = (df['team_score'] == df['opponent_score']).astype(int)
    df['ft_loss'] = (df['team_score'] < df['opponent_score']).astype(int)

    return df


def add_goals(df):
    """Toplam gol sayısını ekle"""
    df = df.copy()

    df["ht_team_scored"] = (df['team_score_1h'] > 0).astype(int)
    df["ht_opponent_scored"] = (df['opponent_score_1h'] > 0).astype(int)

    df["ht2_team_scored"] = (df['team_score_2h'] > 0).astype(int)
    df["ht2_opponent_scored"] = (df['opponent_score_2h'] > 0).astype(int)

    #ev attı binary ve astype int ile
    df["team_scored"] = (df['team_score'] > 0).astype(int)
    df["opponent_scored"] = (df['opponent_score'] > 0).astype(int)


    

    return df



def add_ht_over_under(df):
    """Over/Under bilgisini ekle (kendi içinde total_goals hesaplar)"""
    df = df.copy()
    
    # İlk önce total_goals'u hesapla (başka fonksiyona bağımlı olmamak için)
    total_goals = df['team_score_1h'] + df['opponent_score_1h']
    
    # 0.5 üstü/altı
    df['ht_over_0_5'] = (total_goals > 0.5).astype(int)
    df['ht_under_0_5'] = (total_goals <= 0.5).astype(int)

    # 1.5 üstü/altı
    df['ht_over_1_5'] = (total_goals > 1.5).astype(int)
    df['ht_under_1_5'] = (total_goals <= 1.5).astype(int)

    # 2.5 üstü/altı
    df['ht_over_2_5'] = (total_goals > 2.5).astype(int)
    df['ht_under_2_5'] = (total_goals <= 2.5).astype(int)

    return df



def add_ht2_over_under(df):
    """Over/Under bilgisini ekle (kendi içinde total_goals hesaplar)"""
    df = df.copy()
    
    # İlk önce total_goals'u hesapla (başka fonksiyona bağımlı olmamak için)
    total_goals = df['team_score_2h'] + df['opponent_score_2h']
    
    # 0.5 üstü/altı
    df['ht2_over_0_5'] = (total_goals > 0.5).astype(int)
    df['ht2_under_0_5'] = (total_goals <= 0.5).astype(int)

    # 1.5 üstü/altı
    df['ht2_over_1_5'] = (total_goals > 1.5).astype(int)
    df['ht2_under_1_5'] = (total_goals <= 1.5).astype(int)

    # 2.5 üstü/altı
    df['ht2_over_2_5'] = (total_goals > 2.5).astype(int)
    df['ht2_under_2_5'] = (total_goals <= 2.5).astype(int)

    return df

# ms üst alt fonksiyonu

# Kesin atılan ve yenilen ilk yarı gol sayısı fonksiyonu
def kesin_gol_sayısı(df):
    df = df.copy()

    #attığı gol sayısı
    df['ht_team_gol_sayisi_0'] = (df['team_score_1h'] == 0).astype(int)
    df['ht_team_gol_sayisi_1'] = (df['team_score_1h'] == 1).astype(int)
    df['ht_team_gol_sayisi_2'] = (df['team_score_1h'] == 2).astype(int)
    df['ht_team_gol_sayisi_3plus'] = (df['team_score_1h'] >= 3).astype(int)
    #2 yarı gol sayısı
    df['ht2_team_gol_sayisi_0'] = (df['team_score_2h'] == 0).astype(int)
    df['ht2_team_gol_sayisi_1'] = (df['team_score_2h'] == 1).astype(int)
    df['ht2_team_gol_sayisi_2'] = (df['team_score_2h'] == 2).astype(int)
    df['ht2_team_gol_sayisi_3plus'] = (df['team_score_2h'] >= 3).astype(int)

   # ilk yarı 1 yenilen gol 
    df['ht_opponent_gol_sayisi_0'] = (df['opponent_score_1h'] == 0).astype(int)
    df['ht_opponent_gol_sayisi_1'] = (df['opponent_score_1h'] == 1).astype(int)
    df['ht_opponent_gol_sayisi_2'] = (df['opponent_score_1h'] == 2).astype(int)
    df['ht_opponent_gol_sayisi_3plus'] = (df['opponent_score_1h'] >= 3).astype(int)
    #2 yarı gol sayısı
    df['ht2_opponent_gol_sayisi_0'] = (df['opponent_score_2h'] == 0).astype(int)
    df['ht2_opponent_gol_sayisi_1'] = (df['opponent_score_2h'] == 1).astype(int)
    df['ht2_opponent_gol_sayisi_2'] = (df['opponent_score_2h'] == 2).astype(int)
    df['ht2_opponent_gol_sayisi_3plus'] = (df['opponent_score_2h'] >= 3).astype(int)

    # maç sonucu atılan ve yenilen gol sayısı
    df['match_team_gol_sayisi_0'] = (df['team_score'] == 0).astype(int)
    df['match_team_gol_sayisi_1'] = (df['team_score'] == 1).astype(int)
    df['match_team_gol_sayisi_2'] = (df['team_score'] == 2).astype(int)
    df['match_team_gol_sayisi_3plus'] = (df['team_score'] >= 3).astype(int)


    df['match_opponent_gol_sayisi_0'] = (df['opponent_score'] == 0).astype(int)
    df['match_opponent_gol_sayisi_1'] = (df['opponent_score'] == 1).astype(int)
    df['match_opponent_gol_sayisi_2'] = (df['opponent_score'] == 2).astype(int)
    df['match_opponent_gol_sayisi_3plus'] = (df['opponent_score'] >= 3).astype(int)


    return df

def add_fulltime_over_under(df):
    """Fulltime Over/Under bilgisini ekle (kendi içinde total_goals hesaplar)"""
    df = df.copy()
    
    # İlk önce total_goals'u hesapla (başka fonksiyona bağımlı olmamak için)
    total_goals = df['team_score'] + df['opponent_score']
    
    # 0.5 üstü/altı
    df['ft_over_0_5'] = (total_goals > 0.5).astype(int)
    df['ft_under_0_5'] = (total_goals <= 0.5).astype(int)

    # 1.5 üstü/altı
    df['ft_over_1_5'] = (total_goals > 1.5).astype(int)
    df['ft_under_1_5'] = (total_goals <= 1.5).astype(int)

    # 2.5 üstü/altı
    df['ft_over_2_5'] = (total_goals > 2.5).astype(int)
    df['ft_under_2_5'] = (total_goals <= 2.5).astype(int)

    # 3.5 üstü/altı
    df['ft_over_3_5'] = (total_goals > 3.5).astype(int)
    df['ft_under_3_5'] = (total_goals <= 3.5).astype(int)

    # 4.5 üstü/altı
    df['ft_over_4_5'] = (total_goals > 4.5).astype(int)
    df['ft_under_4_5'] = (total_goals <= 4.5).astype(int)   
    
    return df


# ht kg var mı fonksiyonu

def add_ht_kg(df):
    """İlk yarı karşılıklı gol var mı?"""
    df = df.copy()
    df['ht_kgvar'] = ((df['team_score_1h'] > 0) & (df['opponent_score_1h'] > 0)).astype(int)
    df['ht_kgyok'] = ((df['team_score_1h'] == 0) | (df['opponent_score_1h'] == 0)).astype(int)
    return df   


#maç sonucu var mı fonksiyonu

def add_match_result_kg(df):
    """Maç sonucu var mı?"""
    df = df.copy()
    df['match_result_kgvar'] = ((df['team_score'] > 0) & (df['opponent_score'] > 0)).astype(int)
    df['match_result_kgyok'] = ((df['team_score'] == 0) | (df['opponent_score'] == 0)).astype(int)
    return df   


# şimdi burada koşulluj bir işlem yapacğaız eğer maç üst olduysa bunu team mı yaptı yoksa opponent mı yaptı gibi
# burada kural şu kontol edilecek eğer maç üst ise ve team_score > opponent_score ise team over yapmış demektir
# değilse opponent over yapmış demektir bunu binary olarak ekleyeceğiz 

def kim_2_5_ust_yaptı(df, threshold=2.5):
    """Maçta over yapan takım/opponent bilgisini ekle"""
    df = df.copy()
    
    # Toplam gol sayısını hesapla
    total_goals = df['team_score'] + df['opponent_score']
    

    # Hangi taraf over yaptı?
    df['team_over_2_5_ok'] = ((total_goals > threshold) & (df['team_score'] > df['opponent_score'])).astype(int)
    df['opponent_over_2_5_ok'] = ((total_goals > threshold) & (df['opponent_score'] > df['team_score'])).astype(int)

    return df


# ilk yarıda takımın gol attığı ama yemediği takımın gol yediği atmadığı takımın golsüz maç sayısı ve takımın hem attığı hem yediği

def ht_gol_analiz(df):
    """İlk yarı gol analizini ekle"""
    df = df.copy()

    df['ht_team_scored_only'] = ((df['team_score_1h'] > 0) & (df['opponent_score_1h'] == 0)).astype(int)
    df['ht_opponent_scored_only'] = ((df['opponent_score_1h'] > 0) & (df['team_score_1h'] == 0)).astype(int)
    df['ht_both_scored'] = ((df['team_score_1h'] > 0) & (df['opponent_score_1h'] > 0)).astype(int)
    df['ht_no_goals'] = ((df['team_score_1h'] == 0) & (df['opponent_score_1h'] == 0)).astype(int)

    return df

# sadecde ikinci yarıda takımın gol attığı ama yemediği takımın gol yediği atmadığı takımın golsüz maç sayısı ve takımın hem attığı hem yediği

def ht2_gol_analiz(df):
    """İkinci yarı gol analizini ekle"""
    df = df.copy()

    df['ht2_team_scored_only'] = ((df['team_score_2h'] > 0) & (df['opponent_score_2h'] == 0)).astype(int)
    df['ht2_opponent_scored_only'] = ((df['opponent_score_2h'] > 0) & (df['team_score_2h'] == 0)).astype(int)
    df['ht2_both_scored'] = ((df['team_score_2h'] > 0) & (df['opponent_score_2h'] > 0)).astype(int)
    df['ht2_no_goals'] = ((df['team_score_2h'] == 0) & (df['opponent_score_2h'] == 0)).astype(int)

    return df


# smaç sonunda takımın gol attığı ama yemediği takımın gol yediği atmadığı takımın golsüz maç sayısı ve takımın hem attığı hem yediği

def match_gol_analiz(df):
    """Maç sonu gol analizini ekle"""
    df = df.copy()

    df['match_team_scored_only'] = ((df['team_score'] > 0) & (df['opponent_score'] == 0)).astype(int)
    df['match_opponent_scored_only'] = ((df['opponent_score'] > 0) & (df['team_score'] == 0)).astype(int)
    df['match_both_scored'] = ((df['team_score'] > 0) & (df['opponent_score'] > 0)).astype(int)
    df['match_no_goals'] = ((df['team_score'] == 0) & (df['opponent_score'] == 0)).astype(int)

    return df


# ============================================================================
# YENİ GELİŞMİŞ İSTATİSTİK FONKSİYONLARI
# ============================================================================


def add_clean_sheet_stats(df):
    """
    🛡️ CLEAN SHEET (SIFIR YİYEN) İSTATİSTİKLERİ
    ===========================================
    
    Takımın ve rakibin sıfır gol yediği maçları hesaplar.
    """
    df = df.copy()
    
    # Tam maç clean sheet
    df['team_clean_sheet'] = (df['opponent_score'] == 0).astype(int)
    df['opponent_clean_sheet'] = (df['team_score'] == 0).astype(int)
    
    # İlk yarı clean sheet
    df['ht_team_clean_sheet'] = (df['opponent_score_1h'] == 0).astype(int)
    df['ht_opponent_clean_sheet'] = (df['team_score_1h'] == 0).astype(int)
    
    # İkinci yarı clean sheet
    df['ht2_team_clean_sheet'] = (df['opponent_score_2h'] == 0).astype(int)
    df['ht2_opponent_clean_sheet'] = (df['team_score_2h'] == 0).astype(int)
    
    return df


def add_comeback_stats(df):
    """
    🔄 COMEBACK (GERİ DÖNÜŞ) İSTATİSTİKLERİ
    ======================================
    
    İlk yarı geride başlayıp maçı kazanan veya berabere bitiren durumları hesaplar.
    """
    df = df.copy()
    
    # İlk yarı gerideyken maçı kazanma
    df['comeback_win'] = (
        (df['team_score_1h'] < df['opponent_score_1h']) & 
        (df['team_score'] > df['opponent_score'])
    ).astype(int)
    
    # İlk yarı gerideyken berabere bitirme
    df['comeback_draw'] = (
        (df['team_score_1h'] < df['opponent_score_1h']) & 
        (df['team_score'] == df['opponent_score'])
    ).astype(int)
    
    # İlk yarı öndeyken maçı kaybetme
    df['lead_lost'] = (
        (df['team_score_1h'] > df['opponent_score_1h']) & 
        (df['team_score'] < df['opponent_score'])
    ).astype(int)
    
    # İlk yarı berabere ikinci yarı kazanma
    df['draw_to_win'] = (
        (df['team_score_1h'] == df['opponent_score_1h']) & 
        (df['team_score'] > df['opponent_score'])
    ).astype(int)
    
    return df


def add_scoring_patterns(df):
    """
    ⚽ GOL ATMA PATTERN'LERİ
    =======================
    
    Hangi yarıda daha çok gol attığını ve gol dağılımını analiz eder.
    """
    df = df.copy()
    
    # Sadece ilk yarıda gol atma
    df['scored_only_1h'] = (
        (df['team_score_1h'] > 0) & 
        (df['team_score_2h'] == 0)
    ).astype(int)
    
    # Sadece ikinci yarıda gol atma
    df['scored_only_2h'] = (
        (df['team_score_1h'] == 0) & 
        (df['team_score_2h'] > 0)
    ).astype(int)
    
    # Her iki yarıda da gol atma
    df['scored_both_halves'] = (
        (df['team_score_1h'] > 0) & 
        (df['team_score_2h'] > 0)
    ).astype(int)
    
    # Hiçbir yarıda gol atamama
    df['scored_no_half'] = (
        (df['team_score_1h'] == 0) & 
        (df['team_score_2h'] == 0)
    ).astype(int)
    
    # İlk yarıda rakipten fazla gol
    df['ht_more_goals_than_opponent'] = (
        df['team_score_1h'] > df['opponent_score_1h']
    ).astype(int)
    
    # İkinci yarıda rakipten fazla gol
    df['ht2_more_goals_than_opponent'] = (
        df['team_score_2h'] > df['opponent_score_2h']
    ).astype(int)
    
    return df


def add_goal_difference_categories(df):
    """
    📊 GOL FARKI KATEGORİLERİ
    =========================
    
    Maç sonuçlarını gol farkına göre kategorize eder.
    """
    df = df.copy()
    
    # Gol farkını hesapla
    df['goal_difference'] = df['team_score'] - df['opponent_score']
    
    # Farklı galibiyet
    df['win_by_1'] = ((df['goal_difference'] == 1)).astype(int)
    df['win_by_2'] = ((df['goal_difference'] == 2)).astype(int)
    df['win_by_3plus'] = ((df['goal_difference'] >= 3)).astype(int)
    
    # Farklı mağlubiyet
    df['loss_by_1'] = ((df['goal_difference'] == -1)).astype(int)
    df['loss_by_2'] = ((df['goal_difference'] == -2)).astype(int)
    df['loss_by_3plus'] = ((df['goal_difference'] <= -3)).astype(int)
    
    # Beraberlik türleri
    df['draw_0_0'] = ((df['team_score'] == 0) & (df['opponent_score'] == 0)).astype(int)
    df['draw_1_1'] = ((df['team_score'] == 1) & (df['opponent_score'] == 1)).astype(int)
    df['draw_2_2plus'] = (
        (df['team_score'] == df['opponent_score']) & 
        (df['team_score'] >= 2)
    ).astype(int)
    
    return df


def add_high_scoring_stats(df):
    """
    🎯 YÜKSEK SKORLU MAÇ İSTATİSTİKLERİ
    ==================================
    
    Yüksek skorlu maçları ve gol şovlarını analiz eder.
    """
    df = df.copy()
    
    total_goals = df['team_score'] + df['opponent_score']
    
    # Yüksek skorlu maçlar
    df['high_scoring_5plus'] = (total_goals >= 5).astype(int)
    df['high_scoring_6plus'] = (total_goals >= 6).astype(int)
    df['high_scoring_7plus'] = (total_goals >= 7).astype(int)
    
    # Tek taraflı maçlar
    df['one_sided_match'] = (
        ((df['team_score'] >= 3) & (df['opponent_score'] == 0)) |
        ((df['opponent_score'] >= 3) & (df['team_score'] == 0))
    ).astype(int)
    
    # Gol düellosu (her iki takım 2+ gol)
    df['goal_fest'] = (
        (df['team_score'] >= 2) & 
        (df['opponent_score'] >= 2)
    ).astype(int)
    
    return df


def add_late_goal_stats(df):
    """
    ⏰ GEÇ GOL İSTATİSTİKLERİ
    ========================
    
    İkinci yarıda atılan golleri ve geç gol etkilerini analiz eder.
    """
    df = df.copy()
    
    # İkinci yarıda daha fazla gol
    df['more_goals_2h'] = (df['team_score_2h'] > df['team_score_1h']).astype(int)
    df['opponent_more_goals_2h'] = (df['opponent_score_2h'] > df['opponent_score_1h']).astype(int)
    
    # İkinci yarıda yıkılma (3+ gol yeme)
    df['collapsed_2h'] = (df['opponent_score_2h'] >= 3).astype(int)
    
    # İkinci yarıda patlama (3+ gol atma)
    df['exploded_2h'] = (df['team_score_2h'] >= 3).astype(int)
    
    # İkinci yarıda momentum kazanma
    df['momentum_gained'] = (
        (df['team_score_2h'] > df['opponent_score_2h']) &
        (df['team_score_1h'] <= df['opponent_score_1h'])
    ).astype(int)
    
    # İkinci yarıda momentum kaybetme
    df['momentum_lost'] = (
        (df['team_score_2h'] < df['opponent_score_2h']) &
        (df['team_score_1h'] >= df['opponent_score_1h'])
    ).astype(int)
    
    return df


def add_defensive_strength_stats(df):
    """
    🛡️ SAVUNMA GÜCÜ İSTATİSTİKLERİ
    ==============================
    
    Savunma performansını detaylı analiz eder.
    """
    df = df.copy()
    
    # Az gol yeme kategorileri
    df['conceded_0'] = (df['opponent_score'] == 0).astype(int)
    df['conceded_1'] = (df['opponent_score'] == 1).astype(int)
    df['conceded_2plus'] = (df['opponent_score'] >= 2).astype(int)
    df['conceded_3plus'] = (df['opponent_score'] >= 3).astype(int)
    
    # İlk yarı savunma
    df['ht_conceded_0'] = (df['opponent_score_1h'] == 0).astype(int)
    df['ht_conceded_1plus'] = (df['opponent_score_1h'] >= 1).astype(int)
    
    # İkinci yarı savunma
    df['ht2_conceded_0'] = (df['opponent_score_2h'] == 0).astype(int)
    df['ht2_conceded_1plus'] = (df['opponent_score_2h'] >= 1).astype(int)
    
    return df


def add_offensive_power_stats(df):
    """
    ⚔️ HÜCUM GÜCÜ İSTATİSTİKLERİ
    ===========================
    
    Hücum performansını detaylı analiz eder.
    """
    df = df.copy()
    
    # Çok gol atma kategorileri
    df['scored_3plus'] = (df['team_score'] >= 3).astype(int)
    df['scored_4plus'] = (df['team_score'] >= 4).astype(int)
    df['scored_5plus'] = (df['team_score'] >= 5).astype(int)
    
    # İlk yarı hücum gücü
    df['ht_scored_2plus'] = (df['team_score_1h'] >= 2).astype(int)
    df['ht_scored_3plus'] = (df['team_score_1h'] >= 3).astype(int)
    
    # İkinci yarı hücum gücü
    df['ht2_scored_2plus'] = (df['team_score_2h'] >= 2).astype(int)
    df['ht2_scored_3plus'] = (df['team_score_2h'] >= 3).astype(int)
    
    # Etkili hücum (rakipten fazla gol)
    df['effective_attack'] = (df['team_score'] > df['opponent_score']).astype(int)
    df['dominant_attack'] = (df['team_score'] >= df['opponent_score'] + 2).astype(int)
    
    return df


def add_all_advanced_stats(df):
    """
    🎯 TÜM GELİŞMİŞ İSTATİSTİKLERİ EKLE
    ===================================
    
    Yukarıdaki tüm gelişmiş istatistik fonksiyonlarını tek seferde uygular.
    
    Kullanım:
        df = add_all_advanced_stats(df)
    """
    df = df.copy()
    
    # Tüm gelişmiş istatistikleri ekle
    df = add_clean_sheet_stats(df)
    df = add_comeback_stats(df)
    df = add_scoring_patterns(df)
    df = add_goal_difference_categories(df)
    df = add_high_scoring_stats(df)
    df = add_late_goal_stats(df)
    df = add_defensive_strength_stats(df)
    df = add_offensive_power_stats(df)
    
    return df



# Diğer özel fonksiyonlarını buraya ekleyebilirsin


