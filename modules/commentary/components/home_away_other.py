"""
9️⃣ DİĞER İSTATİSTİKLER - Other Stats Component - KOMPAKT
========================================================
"""

def generate_home_away_other_commentary(row):
    """Diğer istatistikler yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # GALİBİYET/BERABERLIK/YENİLGİ
    wins = int(row['sum_all_sum_ft_win'])
    draws = int(row['sum_all_sum_ft_draw'])
    losses = int(row['sum_all_sum_ft_loss'])
    
    if wins > 0 or draws > 0 or losses > 0:
        total_points = wins * 3 + draws
        avg_points = total_points / matches
        
        commentary.append(f"Form: {wins}G-{draws}B-{losses}Y, {avg_points:.1f} puan/maç.")
        
        # Form durumu
        if avg_points >= 2.5:
            commentary.append("Şampiyonluk formu.")
        elif avg_points >= 2.0:
            commentary.append("Çok iyi dönem.")
        elif avg_points < 1.0:
            commentary.append("Kötü form, kriz.")
    
    # GOL FARKI
    goals_scored = float(row['sum_all_sum_team_score'])
    goals_conceded = float(row['sum_all_sum_opponent_score'])
    
    if goals_scored > 0 or goals_conceded > 0:
        goal_diff = goals_scored - goals_conceded
        
        if goal_diff > 10:
            commentary.append(f"Gol farkı: +{int(goal_diff)} → artı 10 üstü averaj var.")
        elif goal_diff > 5:
            commentary.append(f"Gol farkı: +{int(goal_diff)} → artı 5 üstü averaj var.")
        elif goal_diff < -10:
            commentary.append(f"Gol farkı: {int(goal_diff)} → -10 averaj altında, ciddi kriz.")
        elif goal_diff < -5:
            commentary.append(f"Gol farkı: {int(goal_diff)} → -5 averaj altında, zayıf performans.")
        elif goal_diff == 0:
            commentary.append("Gol farkı: 0 → Dengeli.")
    
    return " ".join(commentary)
