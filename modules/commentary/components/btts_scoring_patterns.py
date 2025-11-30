"""
🎲 BTTS & SKORLAMA PATERNLERİ - BTTS & Scoring Patterns Component
=================================================================

Karşılıklı gol (BTTS), yarı bazlı skorlama, gol zamanlaması.
AI'nın maç dinamiklerini DETAYLI anlamasını sağlar.
"""

def generate_btts_scoring_patterns_commentary(row):
    """BTTS ve skorlama paterni analizi"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # KARŞILIKLI GOL (BTTS)
    both_scored = int(row.get('sum_all_sum_match_both_scored', 0))
    no_goals = int(row.get('sum_all_sum_match_no_goals', 0))
    team_scored_only = int(row.get('sum_all_sum_match_team_scored_only', 0))
    opponent_scored_only = int(row.get('sum_all_sum_match_opponent_scored_only', 0))
    
    if both_scored > 0:
        pct = (both_scored / matches) * 100
        commentary.append(f"BTTS: {both_scored}×/%{pct:.0f}.")
        
        if pct > 60:
            commentary.append("Çok açık maçlar → Her iki takım gol atıyor.")
    
    if no_goals > 0:
        pct = (no_goals / matches) * 100
        commentary.append(f"Golsüz: {no_goals}×/%{pct:.0f}.")
        
        if pct > 30:
            commentary.append("Sık golsüz → Savunma oyunu.")
    
    if team_scored_only > 0:
        pct = (team_scored_only / matches) * 100
        commentary.append(f"Sadece bu takım attı: {team_scored_only}×/%{pct:.0f} → Defans sağlam.")
    
    if opponent_scored_only > 0:
        pct = (opponent_scored_only / matches) * 100
        commentary.append(f"Sadece rakip attı: {opponent_scored_only}×/%{pct:.0f} → Hücum krizi.")
    
    # YARI BAZLI SKORLAMA
    scored_both_halves = int(row.get('sum_all_sum_scored_both_halves', 0))
    scored_no_half = int(row.get('sum_all_sum_scored_no_half', 0))
    scored_only_1h = int(row.get('sum_all_sum_scored_only_1h', 0))
    scored_only_2h = int(row.get('sum_all_sum_scored_only_2h', 0))
    
    if scored_both_halves > 0:
        pct = (scored_both_halves / matches) * 100
        commentary.append(f"Her yarı gol: {scored_both_halves}×/%{pct:.0f}.")
        
        if pct > 50:
            commentary.append("Çok istikrarlı → 90 dakika gol tehdidi.")
    
    if scored_only_1h > 0:
        pct = (scored_only_1h / matches) * 100
        commentary.append(f"Sadece 1.yarı: {scored_only_1h}×/%{pct:.0f}.")
        
        if pct > 30:
            commentary.append("Erken gol ama finish zayıf.")
    
    if scored_only_2h > 0:
        pct = (scored_only_2h / matches) * 100
        commentary.append(f"Sadece 2.yarı: {scored_only_2h}×/%{pct:.0f}.")
        
        if pct > 30:
            commentary.append("Yavaş başlıyor, geç gol atıyor.")
    
    if scored_no_half > 0:
        pct = (scored_no_half / matches) * 100
        commentary.append(f"Hiç gol atmadı: {scored_no_half}×/%{pct:.0f}.")
        
        if pct > 30:
            commentary.append("KRİTİK: Sık golsüz kalıyor.")
    
    # KGVAR/KGYOK (Karşılıklı Gol Var/Yok)
    kgvar = int(row.get('sum_all_sum_match_result_kgvar', 0))
    kgyok = int(row.get('sum_all_sum_match_result_kgyok', 0))
    
    if kgvar > 0 or kgyok > 0:
        total = kgvar + kgyok
        kgvar_pct = (kgvar / total) * 100 if total > 0 else 0
        commentary.append(f"KG oranı: %{kgvar_pct:.0f} KGVAR.")
        
        if kgvar_pct > 70:
            commentary.append("Çok açık oyun → BTTS favorisi.")
        elif kgvar_pct < 30:
            commentary.append("Kapalı maçlar → Bir taraf dominant.")
    
    return " ".join(commentary)
