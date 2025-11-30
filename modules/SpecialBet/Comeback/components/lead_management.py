"""
5️⃣ AVANTAJ YÖNETİMİ ANALİZİ - Lead Management Component
=========================================================

Önde başlayıp kaybetme, avantajı koruma, lead_lost durumları.
Savunma disiplini, maçı öldürme yeteneği.
"""

def generate_lead_management_commentary(stats):
    """
    Avantaj yönetimi yorumu - KRİTİK + UYARICI
    
    Args:
        stats: Team istatistikleri dict
    
    Returns:
        str: Avantaj yönetimi yorumu
    """
    
    matches = int(stats.get('sum_all_matches_played', 0))
    if matches == 0:
        return ""
    
    commentary = []
    
    commentary.append("Şimdi çok kritik bir konu: Önde olduğumda maçı kapatabiliy or muyum yoksa avantajı kaybediyor muyum?")
    
    # ==========================================
    # LEAD LOST (AVANTAJI KAYBETTİM)
    # ==========================================
    lead_lost = int(stats.get('sum_all_sum_lead_lost', 0))
    
    if lead_lost > 0:
        lead_lost_rate = lead_lost / matches * 100
        commentary.append(f"⚠️ DİKKAT! Ben {lead_lost} maçta önce öndeydim ama sonra avantajı kaybettim ve maçı kaybettim (yüzde {lead_lost_rate:.1f}).")
        
        if lead_lost_rate >= 25:
            commentary.append("Bu çok kötü bir istatistik! Maçların çeyreğinde önde olduğum halde sonucu kaybediyorum, bu da ikinci yarıda çok zayıf olduğumu ve avantajı koruyamadığımı gösteriyor, rakipler beni son dakikalarda yakalıyor!")
        elif lead_lost_rate >= 15:
            commentary.append("Bu kötü bir durum, sık sık önde olduğum halde maçı kaybediyorum, ikinci yarıda konsantrasyon kaybı yaşıyorum veya rakipler bana comeback yapıyor.")
        elif lead_lost_rate >= 5:
            commentary.append("Bazen önde olduğum halde maçı kaybediyorum, bu da dikkatli olmam gerektiğini gösteriyor.")
        
        # LEAD LOST vs COMEBACK WIN karşılaştırması
        comeback_win = int(stats.get('sum_all_sum_comeback_win', 0))
        if comeback_win > 0:
            if lead_lost > comeback_win:
                commentary.append(f"İlginç bir durum: Ben rakiplere {lead_lost} kez comeback yaptırırken kendim sadece {comeback_win} kez comeback yaptım, bu da rakiplerin bana comeback yapmasına daha yatkın olduğumu gösteriyor!")
    else:
        commentary.append("✅ Hiçbir maçta avantajı kaybetmedim, önde olduğumda maçı çok iyi koruyorum!")
    
    # ==========================================
    # İLK YARI ÖNDE → MAÇ SONU KAYIP
    # ==========================================
    ht_win = int(stats.get('sum_all_sum_ht_win', 0))
    ft_loss = int(stats.get('sum_all_sum_ft_loss', 0))
    
    if ht_win > 0 and ft_loss > 0:
        # İlk yarı önde olan maçlardan kaç tanesini kaybettik?
        # (Direkt hesaplanamaz ama genel mantık verilebilir)
        commentary.append("İlk yarıyı önde bitirdiğim bazı maçlarda maç sonunda kaybettim, bu da ikinci yarıda çöktüğüm anlamına geliyor.")
    
    # ==========================================
    # WIN BY MARGIN (FARKLI KAZANMALAR)
    # ==========================================
    win_by_1 = int(stats.get('sum_all_sum_win_by_1', 0))
    win_by_2 = int(stats.get('sum_all_sum_win_by_2', 0))
    win_by_3plus = int(stats.get('sum_all_sum_win_by_3plus', 0))
    
    ft_win = int(stats.get('sum_all_sum_ft_win', 0))
    
    if ft_win > 0:
        commentary.append(f"Galibiyetlerime bakarsak {win_by_1} maçı 1 golle, {win_by_2} maçı 2 golle, {win_by_3plus} maçı 3+ golle kazandım.")
        
        if win_by_1 > 0:
            win_by_1_rate = win_by_1 / ft_win * 100
            if win_by_1_rate >= 60:
                commentary.append("Galibiyetlerimin çoğu 1 golle geliyor, bu da maçları zar zor kazandığımı ve son dakikaya kadar belirsizlik olduğunu gösteriyor.")
        
        if win_by_3plus > 0:
            win_by_3plus_rate = win_by_3plus / ft_win * 100
            if win_by_3plus_rate >= 30:
                commentary.append("Sık sık 3+ golle kazanıyorum, bu da rakipleri ezdiğim ve maçları çok rahat bitirdiğim anlamına geliyor!")
    
    # ==========================================
    # LOSS BY MARGIN (FARKLI MAĞLUBİYETLER)
    # ==========================================
    loss_by_1 = int(stats.get('sum_all_sum_loss_by_1', 0))
    loss_by_2 = int(stats.get('sum_all_sum_loss_by_2', 0))
    loss_by_3plus = int(stats.get('sum_all_sum_loss_by_3plus', 0))
    
    if ft_loss > 0:
        commentary.append(f"Mağlubiyetlerime bakarsak {loss_by_1} maçı 1 golle, {loss_by_2} maçı 2 golle, {loss_by_3plus} maçı 3+ golle kaybettim.")
        
        if loss_by_1 > 0:
            loss_by_1_rate = loss_by_1 / ft_loss * 100
            if loss_by_1_rate >= 60:
                commentary.append("Mağlubiyetlerimin çoğu 1 golle geliyor, bu da maçları son dakikaya kadar çekişmeli götürdüğüm ama son anda kaybettiğim anlamına geliyor, biraz daha şanslı olsam sonuç farklı olabilirdi.")
        
        if loss_by_3plus > 0:
            loss_by_3plus_rate = loss_by_3plus / ft_loss * 100
            if loss_by_3plus_rate >= 30:
                commentary.append("Sık sık 3+ golle kaybediyorum, bu da bazı maçlarda çok kötü çöktüğüm ve rakiplerin beni ezdiği anlamına geliyor, bu tarz maçlarda comeback şansım yok!")
    
    # ==========================================
    # DRAW PATTERNS (BERABERLIK PATTERNLERİ)
    # ==========================================
    draw_0_0 = int(stats.get('sum_all_sum_draw_0_0', 0))
    draw_1_1 = int(stats.get('sum_all_sum_draw_1_1', 0))
    draw_2_2plus = int(stats.get('sum_all_sum_draw_2_2plus', 0))
    
    ft_draw = int(stats.get('sum_all_sum_ft_draw', 0))
    
    if ft_draw > 0:
        commentary.append(f"Beraberliklere bakarsak {draw_0_0} maç 0-0, {draw_1_1} maç 1-1, {draw_2_2plus} maç 2-2+ skorla berabere bitti.")
        
        if draw_0_0 > 0 and draw_0_0 / ft_draw >= 0.5:
            commentary.append("Beraberliklerin yarısı 0-0 bitiyor, bu da gol atamadığım ve çekişmeli maçlar oynadığım anlamına geliyor.")
        
        if draw_2_2plus > 0:
            commentary.append(f"{draw_2_2plus} maçta 2-2 veya daha yüksek skorla berabere kaldık, bu da gollü ve hareketli maçlar!")
    
    # ==========================================
    # OPPONENT CLEAN SHEET (RAKİP CLEAN SHEET)
    # ==========================================
    opponent_clean = int(stats.get('sum_all_sum_opponent_clean_sheet', 0))
    
    if opponent_clean > 0:
        opponent_clean_rate = opponent_clean / matches * 100
        commentary.append(f"⚠️ {opponent_clean} maçta rakip clean sheet yaptı (yüzde {opponent_clean_rate:.1f}), yani ben gol atamadım ve rakip gol yemedi.")
        
        if opponent_clean_rate >= 30:
            commentary.append("Çok sık rakipler bana karşı clean sheet yapıyor, bu da gol atmakta çok zorlandığımı gösteriyor, bu durum comeback yapmamı imkansız hale getiriyor!")
    
    return " ".join(commentary)
