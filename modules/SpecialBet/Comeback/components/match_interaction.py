"""
6️⃣ MAÇ ETKİLEŞİM ANALİZİ - Match Interaction Component
========================================================

İki takımın birbirine etkisi, karşılıklı gol, çift taraflı maçlar.
İlk yarı iyi takım vs ikinci yarı iyi takım etkileşimi.
"""

def generate_match_interaction_commentary(home_stats, away_stats, team_type='home'):
    """
    Maç etkileşim yorumu - KARŞILAŞTIRMALI + STRATEJİK
    
    Args:
        home_stats: Ev sahibi istatistikleri dict
        away_stats: Deplasman istatistikleri dict
        team_type: 'home' veya 'away'
    
    Returns:
        str: Maç etkileşim yorumu
    """
    
    my_stats = home_stats if team_type == 'home' else away_stats
    opp_stats = away_stats if team_type == 'home' else home_stats
    
    my_matches = int(my_stats.get('sum_all_matches_played', 0))
    opp_matches = int(opp_stats.get('sum_all_matches_played', 0))
    
    if my_matches == 0 or opp_matches == 0:
        return ""
    
    commentary = []
    
    team_name = "ev sahibi" if team_type == 'home' else "deplasman"
    opp_name = "deplasman" if team_type == 'home' else "ev sahibi"
    
    commentary.append(f"Şimdi ben {team_name} takımı olarak rakibim {opp_name} takımıyla etkileşimimi analiz edelim.")
    
    # ==========================================
    # İLK YARI PERFORMANS KARŞILAŞTIRMASI
    # ==========================================
    my_ht_avg_scored = float(my_stats.get('sum_all_avg_team_score_1h', 0))
    my_ht_avg_conceded = float(my_stats.get('sum_all_avg_opponent_score_1h', 0))
    opp_ht_avg_scored = float(opp_stats.get('sum_all_avg_team_score_1h', 0))
    opp_ht_avg_conceded = float(opp_stats.get('sum_all_avg_opponent_score_1h', 0))
    
    commentary.append(f"İlk yarı performanslarımız: Ben maç başına ortalama {my_ht_avg_scored:.2f} gol atıp {my_ht_avg_conceded:.2f} gol yedim, rakip ise {opp_ht_avg_scored:.2f} gol atıp {opp_ht_avg_conceded:.2f} gol yedi.")
    
    # İLK YARI ETKİLEŞİM ANALİZİ
    if my_ht_avg_scored > opp_ht_avg_conceded * 1.3:
        commentary.append(f"✅ İlk yarıda benim hücumum rakibin savunmasından çok daha güçlü, ben maç başına {my_ht_avg_scored:.2f} gol atarken rakip sadece {opp_ht_avg_conceded:.2f} gol yiyor, ilk yarıda avantaj bende!")
    elif opp_ht_avg_scored > my_ht_avg_conceded * 1.3:
        commentary.append(f"⚠️ Dikkat! İlk yarıda rakibin hücumu benim savunmamdan çok daha tehlikeli, rakip maç başına {opp_ht_avg_scored:.2f} gol atarken ben sadece {my_ht_avg_conceded:.2f} gol yedim, ilk yarıda rakip daha güçlü!")
    else:
        commentary.append("İlk yarıda ikimizin de gücü dengeli görünüyor, çekişmeli bir ilk yarı bekleniyor.")
    
    # ==========================================
    # İKİNCİ YARI PERFORMANS KARŞILAŞTIRMASI
    # ==========================================
    my_ht2_avg_scored = float(my_stats.get('sum_all_avg_team_score_2h', 0))
    my_ht2_avg_conceded = float(my_stats.get('sum_all_avg_opponent_score_2h', 0))
    opp_ht2_avg_scored = float(opp_stats.get('sum_all_avg_team_score_2h', 0))
    opp_ht2_avg_conceded = float(opp_stats.get('sum_all_avg_opponent_score_2h', 0))
    
    commentary.append(f"İkinci yarı performanslarımız: Ben maç başına ortalama {my_ht2_avg_scored:.2f} gol atıp {my_ht2_avg_conceded:.2f} gol yedim, rakip ise {opp_ht2_avg_scored:.2f} gol atıp {opp_ht2_avg_conceded:.2f} gol yedi.")
    
    # İKİNCİ YARI ETKİLEŞİM ANALİZİ
    if my_ht2_avg_scored > opp_ht2_avg_conceded * 1.3:
        commentary.append(f"✅ İkinci yarıda benim hücumum rakibin savunmasından çok daha güçlü, ben maç başına {my_ht2_avg_scored:.2f} gol atarken rakip sadece {opp_ht2_avg_conceded:.2f} gol yiyor, ikinci yarıda avantaj bende!")
    elif opp_ht2_avg_scored > my_ht2_avg_conceded * 1.3:
        commentary.append(f"⚠️ Dikkat! İkinci yarıda rakibin hücumu benim savunmamdan çok daha tehlikeli, rakip maç başına {opp_ht2_avg_scored:.2f} gol atarken ben sadece {my_ht2_avg_conceded:.2f} gol yedim, ikinci yarıda rakip daha güçlü!")
    else:
        commentary.append("İkinci yarıda ikimizin de gücü dengeli görünüyor.")
    
    # ==========================================
    # KRİTİK SENARYO: İLK YARI vs İKİNCİ YARI TERS DÖNMESİ
    # ==========================================
    # Senaryo 1: Ben ilk yarı kötü ama rakip ikinci yarı kötü
    if my_ht_avg_scored < opp_ht_avg_conceded and my_ht2_avg_scored > opp_ht2_avg_conceded * 1.2:
        commentary.append("🔥 KRİTİK SENARYO: Ben ilk yarıda zayıfım ama ikinci yarıda çok güçlüyüm! Rakip ise ikinci yarıda zayıflıyor. Bu maçta ilk yarıyı geride bitirsem bile ikinci yarıda COMEBACK yapma şansım çok yüksek!")
    
    # Senaryo 2: Ben ilk yarı iyi ama ikinci yarı kötü
    if my_ht_avg_scored > opp_ht_avg_conceded * 1.2 and my_ht2_avg_scored < opp_ht2_avg_scored:
        commentary.append("⚠️ TEHLİKELİ SENARYO: Ben ilk yarıda güçlüyüm ama ikinci yarıda zayıflıyorum! Rakip ise ikinci yarıda güçleniyor. İlk yarıyı önde bitirirsem bile ikinci yarıda dikkatli olmalıyım, rakip bana COMEBACK yapabilir!")
    
    # Senaryo 3: İkimiz de ilk yarı iyi
    if my_ht_avg_scored > 0.7 and opp_ht_avg_scored > 0.7:
        commentary.append("⚡ HAREKETLI İLK YARI: İkimiz de ilk yarıda çok gol atıyoruz, ilk yarı çok hareketli ve gollü geçecek!")
    
    # Senaryo 4: İkimiz de ikinci yarı iyi
    if my_ht2_avg_scored > 0.8 and opp_ht2_avg_scored > 0.8:
        commentary.append("⚡ HAREKETLI İKİNCİ YARI: İkimiz de ikinci yarıda çok gol atıyoruz, ikinci yarı çok hareketli geçecek ve son dakika dramları olabilir!")
    
    # ==========================================
    # COMEBACK POTANSİYELİ KARŞILAŞTIRMASI
    # ==========================================
    my_comeback_win = int(my_stats.get('sum_all_sum_comeback_win', 0))
    opp_comeback_win = int(opp_stats.get('sum_all_sum_comeback_win', 0))
    
    my_comeback_rate = (my_comeback_win / my_matches * 100) if my_matches > 0 else 0
    opp_comeback_rate = (opp_comeback_win / opp_matches * 100) if opp_matches > 0 else 0
    
    commentary.append(f"Comeback yeteneklerimiz: Ben yüzde {my_comeback_rate:.1f} oranında comeback yaparken rakip yüzde {opp_comeback_rate:.1f} oranında comeback yapıyor.")
    
    if my_comeback_rate > opp_comeback_rate * 1.5:
        commentary.append("✅ Benim comeback yeteneğim rakibimden çok daha iyi, eğer bu maçta geride kalırsam geri gelme şansım rakipten çok daha yüksek!")
    elif opp_comeback_rate > my_comeback_rate * 1.5:
        commentary.append("⚠️ Rakibin comeback yeteneği benden çok daha iyi, eğer ilk yarıyı önde bitirirsem bile rakip geri gelebilir, dikkatli olmalıyım!")
    
    # ==========================================
    # LEAD LOST KARŞILAŞTIRMASI
    # ==========================================
    my_lead_lost = int(my_stats.get('sum_all_sum_lead_lost', 0))
    opp_lead_lost = int(opp_stats.get('sum_all_sum_lead_lost', 0))
    
    if my_lead_lost > 0 or opp_lead_lost > 0:
        commentary.append(f"Avantajı kaybetme: Ben {my_lead_lost} maçta avantajı kaybettim, rakip ise {opp_lead_lost} maçta avantajı kaybetti.")
        
        if my_lead_lost > opp_lead_lost * 1.5:
            commentary.append("⚠️ Ben rakipten çok daha sık avantajı kaybediyorum, bu da ilk yarıyı önde bitirirsem bile ikinci yarıda dikkatli olmam gerektiğini gösteriyor!")
        elif opp_lead_lost > my_lead_lost * 1.5:
            commentary.append("✅ Rakip benden çok daha sık avantajı kaybediyor, eğer rakip ilk yarıyı önde bitirirse ben ikinci yarıda comeback yapabilirim!")
    
    # ==========================================
    # MOMENTUM KARŞILAŞTIRMASI
    # ==========================================
    my_momentum_gained = int(my_stats.get('sum_all_sum_momentum_gained', 0))
    opp_momentum_gained = int(opp_stats.get('sum_all_sum_momentum_gained', 0))
    
    if my_momentum_gained > opp_momentum_gained * 1.3:
        commentary.append("✅ Ben rakipten çok daha sık momentum kazanıyorum, maçın kontrolünü genellikle ben alıyorum!")
    elif opp_momentum_gained > my_momentum_gained * 1.3:
        commentary.append("⚠️ Rakip benden çok daha sık momentum kazanıyor, maçın kontrolünü rakip daha kolay alabilir!")
    
    # ==========================================
    # GENEL DEĞERLENDİRME
    # ==========================================
    commentary.append("\n" + "="*80)
    commentary.append("📊 GENEL DEĞERLENDİRME:")
    
    # Hangi takım daha güçlü?
    my_ft_win = int(my_stats.get('sum_all_sum_ft_win', 0))
    opp_ft_win = int(opp_stats.get('sum_all_sum_ft_win', 0))
    
    my_win_rate = (my_ft_win / my_matches * 100) if my_matches > 0 else 0
    opp_win_rate = (opp_ft_win / opp_matches * 100) if opp_matches > 0 else 0
    
    if my_win_rate > opp_win_rate * 1.2:
        commentary.append(f"✅ Ben bu maçta favoriyim! Benim galibiyet oranım yüzde {my_win_rate:.1f}, rakibin ise yüzde {opp_win_rate:.1f}.")
    elif opp_win_rate > my_win_rate * 1.2:
        commentary.append(f"⚠️ Rakip bu maçta favori! Rakibin galibiyet oranı yüzde {opp_win_rate:.1f}, benimki ise yüzde {my_win_rate:.1f}.")
    else:
        commentary.append("⚖️ Bu maç çok dengeli görünüyor, her iki takımın da kazanma şansı var!")
    
    return " ".join(commentary)
