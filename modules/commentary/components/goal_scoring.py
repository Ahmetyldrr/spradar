"""
3️⃣ GOL ATMA İSTATİSTİKLERİ - Goal Scoring Component - KOMPAKT
============================================================
"""

def generate_goal_scoring_commentary(row):
    """Gol atma yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # GENEL GOL
    goals_scored = float(row['sum_all_sum_team_score'])
    avg_scored = float(row['sum_all_avg_team_score'])
    
    commentary.append(f"{int(goals_scored)} gol / {avg_scored:.1f} ort.")
    
    # Hücum profili
    if avg_scored >= 2.5:
        commentary.append("Üstün hücum gücü.")
    elif avg_scored >= 1.8:
        commentary.append("Etkili hücum.")
    elif avg_scored < 1.2:
        commentary.append("Gol üretme problemi.")
    
    # GOL DAĞILIMI
    team_0g = int(row['sum_all_sum_match_team_gol_sayisi_0'])
    team_1g = int(row['sum_all_sum_match_team_gol_sayisi_1'])
    team_2g = int(row['sum_all_sum_match_team_gol_sayisi_2'])
    team_3plus = int(row['sum_all_sum_match_team_gol_sayisi_3plus'])
    
    parts = []
    if team_0g > 0: parts.append(f"{team_0g}×0g")
    if team_1g > 0: parts.append(f"{team_1g}×1g")
    if team_2g > 0: parts.append(f"{team_2g}×2g")
    if team_3plus > 0: parts.append(f"{team_3plus}×3+g")
    
    if parts:
        commentary.append(f"Dağılım: {', '.join(parts)}.")
    
    # Kritik metrikler
    if team_0g / matches >= 0.3:
        commentary.append(f"Yüzde {team_0g/matches*100:.0f} golsüz → Hücum krizi.")
    
    if team_3plus / matches >= 0.3:
        commentary.append(f"Yüzde {team_3plus/matches*100:.0f} gol şovu → Patlayıcı.")
    
    # GOL ATMA BAŞARISI
    team_scored = int(row['sum_all_sum_team_scored'])
    team_scored_only = int(row['sum_all_sum_match_team_scored_only'])
    
    commentary.append(f"{team_scored} maç gol attı (%{team_scored/matches*100:.0f}).")
    
    if team_scored_only / matches >= 0.25:
        commentary.append(f"{team_scored_only} maç tek taraflı → Dominant.")
    
    # İSTİKRAR
    if team_scored / matches >= 0.8:
        commentary.append("Gol atma istikrarı yüksek.")
    elif team_scored / matches <= 0.5:
        commentary.append("Gol üretme istikrarsız.")
    
    return " ".join(commentary)

