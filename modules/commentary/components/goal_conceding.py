"""
4️⃣ GOL YEDİRME İSTATİSTİKLERİ - Goal Conceding Component - KOMPAKT
===================================================================
"""

def generate_goal_conceding_commentary(row):
    """Gol yedirme yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # GENEL SAVUNMA
    goals_conceded = float(row['sum_all_sum_opponent_score'])
    avg_conceded = float(row['sum_all_avg_opponent_score'])
    
    commentary.append(f"{int(goals_conceded)} yedi / {avg_conceded:.1f} ort.")
    
    # Savunma profili
    if avg_conceded <= 0.5:
        commentary.append("Demir savunma.")
    elif avg_conceded <= 1.0:
        commentary.append("Sağlam defans.")
    elif avg_conceded >= 2.0:
        commentary.append("Savunma zayıf, çok gol yiyor.")
    
    # RAKİP GOL DAĞILIMI
    opponent_0g = int(row['sum_all_sum_match_opponent_gol_sayisi_0'])
    opponent_1g = int(row['sum_all_sum_match_opponent_gol_sayisi_1'])
    opponent_2g = int(row['sum_all_sum_match_opponent_gol_sayisi_2'])
    opponent_3plus = int(row['sum_all_sum_match_opponent_gol_sayisi_3plus'])
    
    parts = []
    if opponent_0g > 0: parts.append(f"{opponent_0g}×0y")
    if opponent_1g > 0: parts.append(f"{opponent_1g}×1y")
    if opponent_2g > 0: parts.append(f"{opponent_2g}×2y")
    if opponent_3plus > 0: parts.append(f"{opponent_3plus}×3+y")
    
    if parts:
        commentary.append(f"Dağılım: {', '.join(parts)}.")
    
    # CLEAN SHEET
    if opponent_0g / matches >= 0.4:
        commentary.append(f"{opponent_0g} gol yemedi → Yüzde {opponent_0g/matches*100:.0f} clean sheet.")
    
    # ÇÖK ÜŞ
    if opponent_3plus / matches >= 0.25:
        commentary.append(f"{opponent_3plus} maç 3+ yedi → Savunma çöküşü sık.")
    
    # GOL YEDİRME BAŞARISI (Rakip gol attı mı?)
    opponent_scored = int(row['sum_all_sum_opponent_scored'])  # Doğru sütun adı
    
    commentary.append(f"{opponent_scored} maç gol yedi (%{opponent_scored/matches*100:.0f}).")
    
    # İSTİKRAR
    if opponent_0g / matches >= 0.5:
        commentary.append("Temiz çıkma oranı yüksek.")
    elif opponent_scored / matches >= 0.9:
        commentary.append("Hemen her maç gol yiyor → İstikrarsız savunma.")
    
    return " ".join(commentary)
    