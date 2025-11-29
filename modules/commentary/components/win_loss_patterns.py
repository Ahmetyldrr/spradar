"""
⚔️ GALİBİYET/YENİLGİ MARJLARI - Win/Loss Patterns Component
===========================================================

Galibiyet ve yenilgi marjları, tek taraflı maçlar, skorlama derinliği.
AI'nın takımın NASIL kazandığını/kaybettiğini anlamasını sağlar.
"""

def generate_win_loss_patterns_commentary(row):
    """Galibiyet/Yenilgi marjları ve paternler"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # GALİBİYET MARJLARI
    win_by_1 = int(row.get('sum_all_sum_win_by_1', 0))
    win_by_2 = int(row.get('sum_all_sum_win_by_2', 0))
    win_by_3plus = int(row.get('sum_all_sum_win_by_3plus', 0))
    
    total_wins = int(row.get('sum_all_sum_ft_win', 0))
    
    if total_wins > 0:
        commentary.append(f"Galibiyet marjları: 1g→{win_by_1}×, 2g→{win_by_2}×, 3+g→{win_by_3plus}×.")
        
        if win_by_3plus > 0:
            pct = (win_by_3plus / total_wins) * 100
            commentary.append(f"Farklı galibiyet: %{pct:.0f} → Ezici üstünlük.")
        
        if win_by_1 > 0:
            pct = (win_by_1 / total_wins) * 100
            if pct > 60:
                commentary.append("Çoğu galibiyet dar → Maçları zor kazanıyor.")
    
    # YENİLGİ MARJLARI
    loss_by_1 = int(row.get('sum_all_sum_loss_by_1', 0))
    loss_by_2 = int(row.get('sum_all_sum_loss_by_2', 0))
    loss_by_3plus = int(row.get('sum_all_sum_loss_by_3plus', 0))
    
    total_losses = int(row.get('sum_all_sum_ft_loss', 0))
    
    if total_losses > 0:
        commentary.append(f"Yenilgi marjları: 1g→{loss_by_1}×, 2g→{loss_by_2}×, 3+g→{loss_by_3plus}×.")
        
        if loss_by_3plus > 0:
            pct = (loss_by_3plus / total_losses) * 100
            commentary.append(f"Farklı yenilgi: %{pct:.0f} → Ağır dağılmalar.")
        
        if loss_by_1 > 0:
            pct = (loss_by_1 / total_losses) * 100
            if pct > 60:
                commentary.append("Dar yenilgiler → Kayıplar şanssızlık.")
    
    # TEK TARAFLI MAÇLAR
    one_sided = int(row.get('sum_all_sum_one_sided_match', 0))
    
    if one_sided > 0:
        pct = (one_sided / matches) * 100
        commentary.append(f"Tek taraflı maç: {one_sided}×/%{pct:.0f}.")
        
        if pct > 40:
            commentary.append("Çok dominant veya çok zayıf → Dengeli değil.")
    
    return " ".join(commentary)
