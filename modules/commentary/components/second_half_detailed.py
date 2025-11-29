"""
6️⃣ İKİNCİ YARI DETAYLI ANALİZ - Second Half Detailed Component
==============================================================

İkinci yarı performansı, comeback/çöküş analizi - KOMPAKT
"""

def generate_second_half_detailed_commentary(row):
    """İkinci yarı yorumu - KOMPAKT & YOĞUN"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    ht2_team_score = float(row['sum_all_sum_team_score_2h'])
    ht2_opponent_score = float(row['sum_all_sum_opponent_score_2h'])
    
    if ht2_team_score == 0 and ht2_opponent_score == 0:
        return ""
    
    commentary = []
    
    # İKİNCİ YARI SKOR ORTALAMASI
    ht2_avg_team = float(row['sum_all_avg_team_score_2h'])
    ht2_avg_opponent = float(row['sum_all_avg_opponent_score_2h'])
    
    commentary.append(f"2. yarı: {ht2_avg_team:.1f}-{ht2_avg_opponent:.1f} ort.")
    
    # 1. YARI vs 2. YARI KARŞILAŞTIRMA
    ht_avg_team = float(row['sum_all_avg_team_score_1h'])
    ht_avg_opponent = float(row['sum_all_avg_opponent_score_1h'])
    
    if ht2_avg_team > ht_avg_team * 1.3:
        commentary.append("2. yarı patlaması → Maç ilerledikçe açılıyor.")
    elif ht2_avg_team < ht_avg_team * 0.7:
        commentary.append("2. yarı düşüş → Yoruluyor/kapanıyor.")
    
    if ht2_avg_opponent > ht_avg_opponent * 1.3:
        commentary.append("2. yarı savunma zayıflıyor → Geç gol yiyor.")
    
    # GOL DAĞILIMI
    ht2_team_0g = int(row['sum_all_sum_ht2_team_gol_sayisi_0'])
    ht2_team_2plus = int(row['sum_all_sum_ht2_team_gol_sayisi_2'])
    
    if ht2_team_0g / matches >= 0.5:
        commentary.append(f"{ht2_team_0g} maç 2. yarı golsüz → Finish zayıf.")
    
    if ht2_team_2plus / matches >= 0.3:
        commentary.append(f"{ht2_team_2plus} maç 2+ gol → Comeback/finish güçlü.")
    
    # RAKİP GOL ANALİZİ
    ht2_opponent_0g = int(row['sum_all_sum_ht2_opponent_gol_sayisi_0'])
    ht2_opponent_2plus = int(row['sum_all_sum_ht2_opponent_gol_sayisi_2'])
    
    if ht2_opponent_0g / matches >= 0.6:
        commentary.append(f"{ht2_opponent_0g} temiz 2. yarı → Maçı kilitleme iyi.")
    
    if ht2_opponent_2plus / matches >= 0.25:
        commentary.append(f"{ht2_opponent_2plus} maç 2+ yedi → Maç sonu çöküşü.")
    
    # TEMPO
    ht2_over_1_5 = int(row['sum_all_sum_ht2_over_1_5'])
    
    if ht2_over_1_5 / matches >= 0.6:
        commentary.append("2. yarı tempo yüksek, açık oyun.")
    
    # 1H vs 2H TEMPO
    ht_over_1_5 = int(row['sum_all_sum_ht_over_1_5'])
    if ht2_over_1_5 > ht_over_1_5 * 1.2:
        commentary.append("2. yarı çok daha hareketli → Geç açılıyor.")
    elif ht2_over_1_5 < ht_over_1_5 * 0.8:
        commentary.append("2. yarı yavaşlıyor → Kapanıyor.")
    
    # KARŞILIKLI GOL
    ht2_both = int(row['sum_all_sum_ht2_both_scored'])
    if ht2_both / matches >= 0.4:
        commentary.append(f"{ht2_both} maç karşılıklı → Açık finish.")
    
    # HT vs FT GALİBİYET ORANI (Comeback/Çöküş)
    ht_win = int(row['sum_all_sum_ht_win'])
    ft_win = int(row['sum_all_sum_ft_win'])
    
    if ft_win > ht_win * 1.3:
        commentary.append("Devre geride → Maç sonu kazanıyor, comeback çok iyi.")
    elif ft_win < ht_win * 0.8:
        commentary.append("Devre önde → Maç sonu kaybediyor, avantaj korunamıyor.")
    
    return " ".join(commentary)
