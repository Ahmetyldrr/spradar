"""
7️⃣ OVER/UNDER + CLEAN SHEET + COMEBACK - Special Stats Component - KOMPAKT
===========================================================================
"""

def generate_special_stats_commentary(row):
    """Özel istatistikler yorumu - KOMPAKT"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # OVER/UNDER
    over_1_5 = int(row['sum_all_sum_ft_over_1_5'])
    over_2_5 = int(row['sum_all_sum_ft_over_2_5'])
    over_3_5 = int(row['sum_all_sum_ft_over_3_5'])
    over_4_5 = int(row['sum_all_sum_ft_over_4_5'])
    
    under_2_5 = matches - over_2_5
    
    commentary.append(f"Over/Under: {over_2_5}×2.5üst (%{over_2_5/matches*100:.0f}), {under_2_5}×2.5alt.")
    
    # Tempo karakteri
    if over_2_5 / matches >= 0.7:
        commentary.append("Çok gollü maçlar → Yüksek tempo.")
    elif over_2_5 / matches <= 0.3:
        commentary.append("Az gollü maçlar → Düşük tempo.")
    
    # Gol şovu
    if over_4_5 / matches >= 0.15:
        commentary.append(f"{over_4_5} gol şovu (4.5+) → Çılgın maçlar.")
    
    # CLEAN SHEET
    clean_sheet = int(row['sum_all_sum_team_clean_sheet'])
    failed_to_score = int(row['sum_all_sum_match_team_gol_sayisi_0'])
    
    cs_rate = clean_sheet / matches
    fts_rate = failed_to_score / matches
    
    commentary.append(f"Temiz: {clean_sheet} (%{cs_rate*100:.0f}), Golsüz: {failed_to_score} (%{fts_rate*100:.0f}).")
    
    # Analiz
    if cs_rate >= 0.4:
        commentary.append("Yüksek clean sheet → Sağlam defans.")
    elif cs_rate <= 0.2:
        commentary.append("Düşük clean sheet → Her maç gol yiyor.")
    
    if fts_rate >= 0.3:
        commentary.append("Sık golsüz → Hücum krizi.")
    
    if cs_rate <= 0.25 and fts_rate >= 0.3:
        commentary.append("Hem yiyor hem atmıyor → İki uç da kötü.")
    
    # COMEBACK
    comeback_win = int(row['sum_all_sum_comeback_win'])
    comeback_draw = int(row['sum_all_sum_comeback_draw'])
    
    if comeback_win > 0 or comeback_draw > 0:
        total_comeback = comeback_win + comeback_draw
        commentary.append(f"Comeback: {comeback_win}G + {comeback_draw}B = {total_comeback} (%{total_comeback/matches*100:.0f}).")
        
        if total_comeback / matches >= 0.3:
            commentary.append("Sık comeback → Mental güçlü.")
        elif comeback_win == 0:
            commentary.append("0 comeback galibiyet → Geride başlayınca kazanamıyor.")
    
    return " ".join(commentary)
