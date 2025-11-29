"""
5️⃣ İLK YARI DETAYLI ANALİZ - First Half Detailed Component
===========================================================

64 sütunlu ilk yarı istatistikleri + yaratıcı etkileşimli analizler.
İlk yarı performansının maç sonucuna etkisi, momentum analizi.
"""

def generate_first_half_detailed_commentary(row):
    """İlk yarı detaylı yorumu - KOMPAKT & YOĞUN"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    # İlk yarı verisi var mı kontrol et
    ht_team_score = float(row['sum_all_sum_team_score_1h'])
    ht_opponent_score = float(row['sum_all_sum_opponent_score_1h'])
    
    if ht_team_score == 0 and ht_opponent_score == 0:
        return ""
    
    commentary = []
    
    # İLK YARI SKOR ORTALAMASI
    ht_avg_team = float(row['sum_all_avg_team_score_1h'])
    ht_avg_opponent = float(row['sum_all_avg_opponent_score_1h'])
    
    commentary.append(f"İlk yarı: {ht_avg_team:.1f}-{ht_avg_opponent:.1f} ort.")
    
    # Hücum profili
    if ht_avg_team >= 1.5:
        commentary.append("Hızlı başlayan, erken gol bulan profil.")
    elif ht_avg_team < 0.5:
        commentary.append("Maça yavaş başlıyor, ilk 45' zayıf.")
    
    # İLK YARI SONUÇ PATTERNİ
    ht_win = int(row['sum_all_sum_ht_win'])
    ht_draw = int(row['sum_all_sum_ht_draw'])
    ht_lose = int(row['sum_all_sum_ht_loss'])
    
    ht_results = []
    if ht_win > 0: ht_results.append(f"{ht_win} önde")
    if ht_draw > 0: ht_results.append(f"{ht_draw} berabere")
    if ht_lose > 0: ht_results.append(f"{ht_lose} geride")
    
    if ht_results:
        commentary.append(f"Devre: {', '.join(ht_results)}.")
    
    # İlk yarı liderlik oranı
    if ht_win / matches >= 0.6:
        commentary.append("Sık sık önde girdiği için 2. yarı rahat.")
    
    # GOL DAĞILIMI
    ht_team_0g = int(row['sum_all_sum_ht_team_gol_sayisi_0'])
    ht_team_2plus = int(row['sum_all_sum_ht_team_gol_sayisi_2'])
    
    if ht_team_0g / matches >= 0.5:
        commentary.append(f"{ht_team_0g} maç golsüz devre → İkinci yarı zor.")
    
    if ht_team_2plus / matches >= 0.3:
        commentary.append(f"{ht_team_2plus} maçta 2+ gol → Baskın başlangıç.")
    
    # RAKİP GOL PROFİLİ
    ht_opponent_0g = int(row['sum_all_sum_ht_opponent_gol_sayisi_0'])
    ht_opponent_2plus = int(row['sum_all_sum_ht_opponent_gol_sayisi_2'])
    
    if ht_opponent_0g / matches >= 0.6:
        commentary.append(f"{ht_opponent_0g} temiz devre → Savunma erken adapte.")
    
    if ht_opponent_2plus / matches >= 0.25:
        commentary.append(f"{ht_opponent_2plus} maç 2+ yedi → Maça kötü başlıyor.")
    
    # TEMPO ANALİZİ
    ht_over_1_5 = int(row['sum_all_sum_ht_over_1_5'])
    
    if ht_over_1_5 / matches >= 0.6:
        commentary.append("İlk yarı tempolu, 1.5 üst sık.")
    elif ht_over_1_5 / matches <= 0.3:
        commentary.append("İlk yarı yavaş, az gollü.")
    
    # KARŞILIKLI GOL
    ht_both = int(row['sum_all_sum_ht_both_scored'])
    if ht_both / matches >= 0.4:
        commentary.append(f"{ht_both} maç karşılıklı gol → Açık oyun.")
    
    return " ".join(commentary)
 
