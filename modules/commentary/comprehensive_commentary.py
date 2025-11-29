"""
🎯 COMPREHENSIVE TEAM COMMENTARY GENERATOR - Ana Birleştirme Modülü
===================================================================

TÜM 286 SÜTUNU KULLANAN KAPSAMLI TAKIM YORUMU ÜRETİCİSİ

12 farklı komponent dosyasını birleştirerek tek bir akıcı doğal paragraf halinde
kapsamlı takım yorumu oluşturur.

Komponentler:
1. Kimlik Bilgileri (5 sütun)
2. Maç Sonuçları + İnteraktif Analiz (18 sütun)
3. Gol Atma İstatistikleri (70 sütun)
4. Gol Yedirme İstatistikleri (58 sütun)
5. İlk Yarı Detaylı (64 sütun)
6. İkinci Yarı Detaylı (60 sütun)
7. Over/Under + Clean Sheet + Comeback + BTTS (42 sütun)
8. Yüksek Skorlu + Gol Farkı (22 sütun)
9. Ev/Deplasman + Diğer (47 sütun)
10. Momentum & Psikolojik (10 sütun) ⚡ YENİ
11. Galibiyet/Yenilgi Marjları (7 sütun) ⚡ YENİ
12. BTTS & Skorlama Paterni (12 sütun) ⚡ YENİ

TOPLAM: 286+ SÜTUN (tam kapsama + derinlik)
"""

from modules.commentary.components.identity_info import generate_identity_commentary
from modules.commentary.components.match_results import generate_match_results_commentary
from modules.commentary.components.goal_scoring import generate_goal_scoring_commentary
from modules.commentary.components.goal_conceding import generate_goal_conceding_commentary
from modules.commentary.components.first_half_detailed import generate_first_half_detailed_commentary
from modules.commentary.components.second_half_detailed import generate_second_half_detailed_commentary
from modules.commentary.components.special_stats import generate_special_stats_commentary
from modules.commentary.components.high_scoring_goal_diff import generate_high_scoring_goal_diff_commentary
from modules.commentary.components.home_away_other import generate_home_away_other_commentary
from modules.commentary.components.momentum_psychological import generate_momentum_psychological_commentary
from modules.commentary.components.win_loss_patterns import generate_win_loss_patterns_commentary
from modules.commentary.components.btts_scoring_patterns import generate_btts_scoring_patterns_commentary


def generate_comprehensive_natural_commentary(row):
    """
    TÜM 286+ SÜTUNU KULLANAN KAPSAMLI DOĞAL YORUM
    
    12 komponent dosyasını sırayla çağırır ve tüm yorumları
    tek bir akıcı doğal paragraf halinde birleştirir.
    
    Args:
        row: Veritabanı satırı (dict)
    
    Returns:
        str: Kapsamlı doğal takım yorumu (~10,000-15,000 karakter)
    """
    
    # Tüm komponentleri başlıklarıyla birlikte oluştur
    components = []
    
    # 1️⃣ Kimlik Bilgileri
    identity = generate_identity_commentary(row)
    if identity and identity.strip():
        components.append(f"[KİMLİK] {identity}")
    
    # 2️⃣ Maç Sonuçları
    results = generate_match_results_commentary(row)
    if results and results.strip():
        components.append(f"[SONUÇLAR] {results}")
    
    # 3️⃣ Gol Atma
    scoring = generate_goal_scoring_commentary(row)
    if scoring and scoring.strip():
        components.append(f"[GOL ATMA] {scoring}")
    
    # 4️⃣ Gol Yedirme
    conceding = generate_goal_conceding_commentary(row)
    if conceding and conceding.strip():
        components.append(f"[SAVUNMA] {conceding}")
    
    # 5️⃣ İlk Yarı
    first_half = generate_first_half_detailed_commentary(row)
    if first_half and first_half.strip():
        components.append(f"[İLK YARI] {first_half}")
    
    # 6️⃣ İkinci Yarı
    second_half = generate_second_half_detailed_commentary(row)
    if second_half and second_half.strip():
        components.append(f"[İKİNCİ YARI] {second_half}")
    
    # 7️⃣ Özel İstatistikler
    special = generate_special_stats_commentary(row)
    if special and special.strip():
        components.append(f"[ÖZEL] {special}")
    
    # 8️⃣ Yüksek Skor + Gol Farkı
    high_scoring = generate_high_scoring_goal_diff_commentary(row)
    if high_scoring and high_scoring.strip():
        components.append(f"[GOL FARKI] {high_scoring}")
    
    # 9️⃣ Ev/Deplasman
    home_away = generate_home_away_other_commentary(row)
    if home_away and home_away.strip():
        components.append(f"[FORM] {home_away}")
    
    # 🔟 Momentum & Psikolojik ⚡ YENİ
    momentum = generate_momentum_psychological_commentary(row)
    if momentum and momentum.strip():
        components.append(f"[MOMENTUM] {momentum}")
    
    # 1️⃣1️⃣ Galibiyet/Yenilgi Marjları ⚡ YENİ
    win_loss = generate_win_loss_patterns_commentary(row)
    if win_loss and win_loss.strip():
        components.append(f"[MARJLAR] {win_loss}")
    
    # 1️⃣2️⃣ BTTS & Skorlama Paterni ⚡ YENİ
    btts = generate_btts_scoring_patterns_commentary(row)
    if btts and btts.strip():
        components.append(f"[BTTS] {btts}")
    
    # Her bölümü tek satırda birleştir (yeni satır yerine " | " ile ayır)
    comprehensive_commentary = " | ".join(components)
    
    return comprehensive_commentary


def generate_match_commentary_comprehensive(home_team_row, away_team_row, match_info):
    """
    Maç için her iki takımın kapsamlı yorumunu üretir
    
    Args:
        home_team_row: Ev sahibi takım veritabanı satırı
        away_team_row: Deplasman takımı veritabanı satırı
        match_info: Maç bilgileri dict
    
    Returns:
        dict: {
            'home_commentary': str,
            'away_commentary': str,
            'match_info': dict
        }
    """
    
    home_commentary = generate_comprehensive_natural_commentary(home_team_row)
    away_commentary = generate_comprehensive_natural_commentary(away_team_row)


    
    
    return {
        'home_commentary': home_commentary,
        'away_commentary': away_commentary,
        'match_info': match_info
    }
