"""
8️⃣ YÜKSEK SKORLU MAÇLAR + GOL FARKI - KOMPAKT
==============================================
"""

def generate_high_scoring_goal_diff_commentary(row):
    """Gol farkı yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # GOL FARKI
    goal_diff = float(row['sum_all_sum_goal_difference'])
    avg_goal_diff = float(row['sum_all_avg_goal_difference'])
    
    commentary.append(f"Gol farkı: {int(goal_diff)} toplam / {avg_goal_diff:.1f} ort.")
    
    # Baskınlık profili
    if avg_goal_diff >= 1.5:
        commentary.append("Çok dominant → Rakipleri eziyor.")
    elif avg_goal_diff >= 0.5:
        commentary.append("Pozitif fark → Üstün performans.")
    elif avg_goal_diff >= -0.5:
        commentary.append("Dengeli → Atıp yiyor.")
    elif avg_goal_diff < -1.5:
        commentary.append("Çok negatif → Eziliyor.")
    
    return " ".join(commentary)
