"""
4️⃣ MOMENTUM ANALİZİ - Momentum Analysis Component
====================================================

Maçın momentum değişimleri, baskı altında kalma/baskı yapma durumları.
Psikolojik güç, maç kontrolü, tempo değişimleri.
"""

def generate_momentum_analysis_commentary(stats):
    """
    Momentum analizi yorumu - PSİKOLOJİK + DİNAMİK
    
    Args:
        stats: Team istatistikleri dict
    
    Returns:
        str: Momentum analizi yorumu
    """
    
    matches = int(stats.get('sum_all_matches_played', 0))
    if matches == 0:
        return ""
    
    commentary = []
    
    commentary.append("Şimdi maçlardaki momentum değişimlerine ve psikolojik gücüme bakalım.")
    
    # ==========================================
    # MOMENTUM GAINED/LOST
    # ==========================================
    momentum_gained = int(stats.get('sum_all_sum_momentum_gained', 0))
    momentum_lost = int(stats.get('sum_all_sum_momentum_lost', 0))
    
    if momentum_gained > 0 or momentum_lost > 0:
        commentary.append(f"Ben {momentum_gained} maçta momentum kazandım (maçın kontrolünü ele geçirdim), {momentum_lost} maçta momentum kaybettim (kontrolü rakibe kaptırdım).")
        
        if momentum_gained > momentum_lost * 1.5:
            commentary.append("Momentum istatistiklerim harika! Genellikle maçın kontrolünü ben ele alıyorum ve rakibi baskı altında tutuyorum, bu da comeback yapmam gerektiğinde çok yardımcı oluyor.")
        elif momentum_lost > momentum_gained * 1.5:
            commentary.append("Momentum istatistiklerim kötü, sık sık maçın kontrolünü kaybediyorum ve rakipler bana hükmedebiliyor, bu da comeback yapmamı çok zorlaştırıyor.")
        else:
            commentary.append("Momentum istatistiklerim dengeli, bazen kontrolü ben alıyorum bazen rakip, maçlar çekişmeli geçiyor.")
    
    # ==========================================
    # DOMINANT/EFFECTIVE ATTACK
    # ==========================================
    dominant_attack = int(stats.get('sum_all_sum_dominant_attack', 0))
    effective_attack = int(stats.get('sum_all_sum_effective_attack', 0))
    
    if dominant_attack > 0:
        dominant_rate = dominant_attack / matches * 100
        commentary.append(f"Ben {dominant_attack} maçta dominant bir hücum performansı gösterdim (yüzde {dominant_rate:.1f}), yani rakibe hiç nefes aldırmadım!")
        
        if dominant_rate >= 40:
            commentary.append("Maçların neredeyse yarısında çok dominant bir hücum performansı gösteriyorum, rakipler bana karşı kendi sahalarına çekilmek zorunda kalıyor.")
    
    if effective_attack > 0:
        effective_rate = effective_attack / matches * 100
        commentary.append(f"Ben {effective_attack} maçta etkili bir hücum performansı gösterdim (yüzde {effective_rate:.1f}), pozisyonlarımı iyi değerlendirdim.")
    
    # ==========================================
    # ONE SIDED MATCH
    # ==========================================
    one_sided = int(stats.get('sum_all_sum_one_sided_match', 0))
    
    if one_sided > 0:
        one_sided_rate = one_sided / matches * 100
        commentary.append(f"Ben {one_sided} maçta tek taraflı bir galibiyet aldım (yüzde {one_sided_rate:.1f}), yani rakibi ezd im!")
        
        if one_sided_rate >= 30:
            commentary.append("Sık sık tek taraflı galibiyetler alıyorum, rakiplere şans tanımıyorum ve ezici bir oyun sergil iyorum.")
    
    # ==========================================
    # GOAL FEST (GOL DÜELLOLERİ)
    # ==========================================
    goal_fest = int(stats.get('sum_all_sum_goal_fest', 0))
    
    if goal_fest > 0:
        goal_fest_rate = goal_fest / matches * 100
        commentary.append(f"Ben {goal_fest} maçta gol düellosu yaşadım (yüzde {goal_fest_rate:.1f}), yani hem ben hem rakip çok gol attı!")
        
        if goal_fest_rate >= 25:
            commentary.append("Maçlarımda sık sık gol düelloları oluyor, bu da açık oyun oynadığımı ve hem gol attığımı hem gol yediğimi gösteriyor, bu tarz maçlarda comeback şansım yüksek çünkü gol atma gücüm var.")
    
    # ==========================================
    # DRAW TO WIN (BERABEREDEN KAZANMAYA)
    # ==========================================
    draw_to_win = int(stats.get('sum_all_sum_draw_to_win', 0))
    
    if draw_to_win > 0:
        draw_to_win_rate = draw_to_win / matches * 100
        commentary.append(f"Ben {draw_to_win} maçta berabere iken maçı kazanmayı başardım (yüzde {draw_to_win_rate:.1f}).")
        
        if draw_to_win_rate >= 20:
            commentary.append("Berabere olan maçlarda sık sık galibiyeti buluyorum, bu da maçı bitirme gücümün yüksek olduğunu gösteriyor, berabere kalınca pasif oynamıyorum, kazanmak için baskı yapıyorum.")
    
    # ==========================================
    # HIGH SCORING MATCHES
    # ==========================================
    high_scoring_5plus = int(stats.get('sum_all_sum_high_scoring_5plus', 0))
    high_scoring_6plus = int(stats.get('sum_all_sum_high_scoring_6plus', 0))
    
    if high_scoring_5plus > 0:
        high_scoring_rate = high_scoring_5plus / matches * 100
        commentary.append(f"Ben {high_scoring_5plus} maçta 5+ gol olan çılgın maçlar oynadım (yüzde {high_scoring_rate:.1f})!")
        
        if high_scoring_rate >= 20:
            commentary.append("Maçlarımda sık sık 5+ gol oluyor, bu da çok açık ve hareketli bir futbol oynadığımı gösteriyor, bu tarz maçlarda her şey olabilir ve comeback şansım her zaman var!")
    
    if high_scoring_6plus > 0:
        commentary.append(f"Hatta {high_scoring_6plus} maçta 6+ gol oldu, bu tam bir gol şov!")
    
    # ==========================================
    # SCORED ONLY 1H/2H (SADECE BİR YARIDE GOL)
    # ==========================================
    scored_only_1h = int(stats.get('sum_all_sum_scored_only_1h', 0))
    scored_only_2h = int(stats.get('sum_all_sum_scored_only_2h', 0))
    
    if scored_only_2h > scored_only_1h * 1.5:
        commentary.append(f"Dikkat! Ben genellikle sadece ikinci yarıda gol atıyorum ({scored_only_2h} maç), ilk yarıda etkisizim ama ikinci yarıda uyanıyorum, bu da comeback için ideal bir profil!")
    elif scored_only_1h > scored_only_2h * 1.5:
        commentary.append(f"Ben genellikle sadece ilk yarıda gol atıyorum ({scored_only_1h} maç), ikinci yarıda yoruluyorum veya kapanıyorum, bu da comeback yapmamı zorlaştırıyor.")
    
    return " ".join(commentary)
