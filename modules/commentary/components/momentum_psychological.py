"""
🔥 MOMENTUM & PSİKOLOJİK ANALİZ - Momentum & Psychological Component
====================================================================

Maç içi momentum değişimleri, psikolojik güç, hücum kalitesi analizi.
Bu veriler AI'nın takımın GERÇEK GÜCÜNü anlamasını sağlar.
"""

def generate_momentum_psychological_commentary(row):
    """Momentum ve psikolojik analiz yorumu"""
    
    matches = int(row['sum_all_matches_played'])
    if matches == 0:
        return ""
    
    commentary = []
    
    # MOMENTUM GAİN/LOSS
    momentum_gained = int(row.get('sum_all_sum_momentum_gained', 0))
    momentum_lost = int(row.get('sum_all_sum_momentum_lost', 0))
    
    if momentum_gained > 0 or momentum_lost > 0:
        momentum_net = momentum_gained - momentum_lost
        commentary.append(f"Momentum: +{momentum_gained}/-{momentum_lost} (Net: {momentum_net:+d}).")
        
        if momentum_net > 3:
            commentary.append("Mental güç çok yüksek → Maç içi dönüşler çok iyi.")
        elif momentum_net < -3:
            commentary.append("Mental çöküş → Maç kontrolü kaybediyor.")
    
    # LEAD LOST (ÖNDEYKENden Kayıp)
    lead_lost = int(row.get('sum_all_sum_lead_lost', 0))
    if lead_lost > 0:
        pct = (lead_lost / matches) * 100
        commentary.append(f"Önden kaybetti: {lead_lost}×/%{pct:.0f} → Avantaj koruyamıyor!")
        
        if pct > 30:
            commentary.append("KRİTİK SORUN: Önden çok kaybediyor.")
    
    # DRAW TO WIN (Beraberlikten Galibiyet)
    draw_to_win = int(row.get('sum_all_sum_draw_to_win', 0))
    if draw_to_win > 0:
        pct = (draw_to_win / matches) * 100
        commentary.append(f"Beraberlikten kazandı: {draw_to_win}×/%{pct:.0f} → Finish güçlü.")
    
    # HÜCUM KALİTESİ
    dominant_attack = int(row.get('sum_all_sum_dominant_attack', 0))
    effective_attack = int(row.get('sum_all_sum_effective_attack', 0))
    
    if dominant_attack > 0 or effective_attack > 0:
        dominant_pct = (dominant_attack / matches) * 100 if matches > 0 else 0
        effective_pct = (effective_attack / matches) * 100 if matches > 0 else 0
        
        commentary.append(f"Hücum: Dominant {dominant_attack}×/%{dominant_pct:.0f}, Etkili {effective_attack}×/%{effective_pct:.0f}.")
        
        if dominant_pct > 50:
            commentary.append("Hücum çok baskın → Rakip baskı altında.")
        elif effective_pct < 30:
            commentary.append("Hücum etkisiz → Gol yaratmada sıkıntı.")
    
    # COLLAPSED 2H / EXPLODED 2H
    collapsed_2h = int(row.get('sum_all_sum_collapsed_2h', 0))
    exploded_2h = int(row.get('sum_all_sum_exploded_2h', 0))
    
    if collapsed_2h > 0:
        pct = (collapsed_2h / matches) * 100
        commentary.append(f"2. yarı çöküş: {collapsed_2h}×/%{pct:.0f} → Son dakikalar kötü.")
    
    if exploded_2h > 0:
        pct = (exploded_2h / matches) * 100
        commentary.append(f"2. yarı patlama: {exploded_2h}×/%{pct:.0f} → İkinci yarı çok güçlü.")
    
    return " ".join(commentary)
