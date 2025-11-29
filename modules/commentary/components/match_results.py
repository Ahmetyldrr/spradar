"""
2️⃣ MAÇ SONUÇLARI VE PUAN DURUMU - Match Results Component - KOMPAKT
====================================================================
"""

def generate_match_results_commentary(row):
    """Maç sonuçları yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    # Sonuçlar
    wins = int(row['sum_all_sum_ft_win'])
    draws = int(row['sum_all_sum_ft_draw'])
    losses = int(row['sum_all_sum_ft_loss'])
    
    win_rate = wins / matches * 100
    draw_rate = draws / matches * 100
    loss_rate = losses / matches * 100
    
    total_points = wins * 3 + draws
    avg_points = total_points / matches
    
    commentary = []
    
    # Genel sonuç
    commentary.append(f"{wins}G {draws}B {losses}M ({win_rate:.0f}%-{draw_rate:.0f}%-{loss_rate:.0f}%) / {avg_points:.1f} puan ort.")
    
    # Form değerlendirmesi
    if win_rate >= 70:
        commentary.append("Mükemmel form.")
    elif win_rate >= 50:
        commentary.append("İyi dönem.")
    elif win_rate < 33:
        commentary.append("Zayıf performans.")
    
    # Beraberlik analizi
    if draws > 0:
        draw_0_0 = int(row['sum_all_sum_draw_0_0'])
        draw_1_1 = int(row['sum_all_sum_draw_1_1'])
        draw_2_2plus = int(row['sum_all_sum_draw_2_2plus'])
        
        parts = []
        if draw_0_0 > 0: parts.append(f"{draw_0_0}×0-0")
        if draw_1_1 > 0: parts.append(f"{draw_1_1}×1-1")
        if draw_2_2plus > 0: parts.append(f"{draw_2_2plus}×2-2+")
        
        if parts:
            commentary.append(f"Beraberlik: {', '.join(parts)}.")
        
        if draw_0_0 > draws * 0.5:
            commentary.append("yüzde 50 üstü Çoğu golsüz → Savunmacı ama golsüz.")
        elif draw_2_2plus > draws * 0.3:
            commentary.append("Yüksek skorlu → Hücum iyi, defans zayıf.")
    
    # Puan durumu
    if avg_points >= 2.0:
        commentary.append("puan ortalamasıyla Ligde zirve mücadelesi.")
    elif avg_points >= 1.5:
        commentary.append("Üst sıra performansı.")
    elif avg_points < 1.0:
        commentary.append("Düşme hattı mücadelesi.")
    
    return " ".join(commentary)
