"""
2️⃣ İLK YARI COMEBACK ANALİZİ - First Half Comeback Component
==============================================================

İlk yarı performansının comeback üzerindeki etkisi.
İlk yarı önde/geride olma durumları ve bunların maç sonucuna yansıması.
"""

def generate_first_half_comeback_commentary(stats):
    """
    İlk yarı comeback yorumu - ETKİLEŞİMLİ + DETAYLI
    
    Args:
        stats: Team istatistikleri dict
    
    Returns:
        str: İlk yarı comeback yorumu
    """
    
    matches = int(stats.get('sum_all_matches_played', 0))
    if matches == 0:
        return ""
    
    commentary = []
    
    commentary.append("Şimdi ilk yarı performansımın comeback yeteneğime nasıl etki ettiğine bakalım.")
    
    # ==========================================
    # İLK YARI SONUÇ DAĞILIMI
    # ==========================================
    ht_win = int(stats.get('sum_all_sum_ht_win', 0))
    ht_draw = int(stats.get('sum_all_sum_ht_draw', 0))
    ht_loss = int(stats.get('sum_all_sum_ht_loss', 0))
    
    commentary.append(f"İlk yarı sonuçlarıma bakarsak {ht_win} maçta öndeydim, {ht_draw} maçta berabereydim, {ht_loss} maçta gerideydim.")
    
    # ==========================================
    # İLK YARI ÖNDE → MAÇ SONU
    # ==========================================
    ft_win = int(stats.get('sum_all_sum_ft_win', 0))
    
    if ht_win > 0:
        ht_win_rate = ht_win / matches * 100
        commentary.append(f"Maçlarımın yüzde {ht_win_rate:.1f}'inde ilk yarıyı önde bitirdim.")
        
        if ht_win_rate >= 50:
            commentary.append("Maçların yarısından fazlasında ilk yarıyı önde bitiriyorum, bu da erken gol bulma yeteneğim olduğunu gösteriyor.")
        elif ht_win_rate >= 30:
            commentary.append("Maçların yaklaşık üçte birinde ilk yarıyı önde bitiriyorum, maça hızlı başlayabiliyorum.")
        
        # İlk yarı önde → Maç sonu kazanma oranı
        if ht_win > 0 and ft_win > 0:
            ht_win_to_ft_win_rate = (ft_win / ht_win) * 100 if ht_win <= ft_win else 100
            commentary.append(f"İlk yarıyı önde bitirdiğim {ht_win} maçın yüzde {ht_win_to_ft_win_rate:.1f}'ini kazandım.")
            
            if ht_win_to_ft_win_rate >= 80:
                commentary.append("İlk yarı önde olduğumda neredeyse her zaman maçı kazanıyorum, avantajı çok iyi koruyorum ve rakibin comeback yapmasına izin vermiyorum.")
            elif ht_win_to_ft_win_rate >= 60:
                commentary.append("İlk yarı önde olduğumda genellikle maçı kazanıyorum ama bazen avantajı kaybedebiliyorum.")
            else:
                commentary.append("İlk yarı önde olsam bile maçı kazanmakta zorlanıyorum, bu da ikinci yarıda problemler yaşadığımı gösteriyor.")
    
    # ==========================================
    # İLK YARI GERİDE → COMEBACK YAPMA
    # ==========================================
    comeback_win = int(stats.get('sum_all_sum_comeback_win', 0))
    comeback_draw = int(stats.get('sum_all_sum_comeback_draw', 0))
    
    if ht_loss > 0:
        ht_loss_rate = ht_loss / matches * 100
        commentary.append(f"Maçlarımın yüzde {ht_loss_rate:.1f}'inde ilk yarıyı geride bitirdim, bu zor bir durum.")
        
        if ht_loss_rate >= 40:
            commentary.append("Maçların neredeyse yarısında ilk yarıyı geride bitiriyorum, bu da maça çok yavaş başladığımı gösteriyor, bu benim için ciddi bir problem.")
        
        # İlk yarı geride → Comeback başarısı
        total_comeback_from_ht_loss = comeback_win + comeback_draw
        if ht_loss > 0 and total_comeback_from_ht_loss > 0:
            comeback_success_rate = (total_comeback_from_ht_loss / ht_loss) * 100
            commentary.append(f"İlk yarıyı geride bitirdiğim {ht_loss} maçın {total_comeback_from_ht_loss} tanesinde geri geldim (yüzde {comeback_success_rate:.1f}).")
            
            if comeback_success_rate >= 50:
                commentary.append("İlk yarı geride olsam bile yarısından fazlasında geri geliyorum, bu inanılmaz bir ikinci yarı gücü! Soyunma odasında çok iyi motivasyon konuşmaları yapılıyor ve ikinci yarıda bambaşka bir takım oluyorum.")
            elif comeback_success_rate >= 30:
                commentary.append("İlk yarı geride olduğumda üçte birinde geri gelebiliyorum, bu kötü değil ama daha iyi olabilir.")
            else:
                commentary.append("İlk yarı geride kaldığımda geri gelmekte çok zorlanıyorum, genellikle maçı kaybediyorum.")
        else:
            commentary.append("İlk yarıyı geride bitirdiğim maçların hiçbirinde geri gelemedim, bu da mental gücümün yetersiz olduğunu gösteriyor.")
    
    # ==========================================
    # İLK YARI BERABERE → MAÇ SONU
    # ==========================================
    if ht_draw > 0:
        ht_draw_rate = ht_draw / matches * 100
        commentary.append(f"Maçlarımın yüzde {ht_draw_rate:.1f}'inde ilk yarı berabere bitti.")
        
        if ht_draw_rate >= 40:
            commentary.append("Maçların neredeyse yarısı ilk yarı berabere bitiyor, bu da çok dengeli maçlar oynadığımı gösteriyor.")
        
        # İlk yarı berabere → İkinci yarı kazanma
        ft_win = int(stats.get('sum_all_sum_ft_win', 0))
        if ht_draw > 0 and ft_win > 0:
            # İlk yarı berabere olan maçlardan kaç tanesini kazandık?
            # (Bu direkt hesaplanamaz, tahmini oran verelim)
            commentary.append("İlk yarı berabere olan maçlarda ikinci yarıda maçı kilitlemem gerekiyor.")
    
    # ==========================================
    # İLK YARI GOL ATMAK → COMEBACK İHTİYACI
    # ==========================================
    ht_team_0_gol = int(stats.get('sum_all_sum_ht_team_gol_sayisi_0', 0))
    
    if ht_team_0_gol > 0:
        ht_no_goal_rate = ht_team_0_gol / matches * 100
        commentary.append(f"İlk yarıda {ht_team_0_gol} maçta hiç gol atamadım (yüzde {ht_no_goal_rate:.1f}).")
        
        if ht_no_goal_rate >= 40:
            commentary.append("Maçların neredeyse yarısında ilk yarıda gol atamıyorum, bu da ikinci yarıda çok fazla baskı altında olduğum ve comeback yapmam gerektiği anlamına geliyor, bu benim için büyük bir dezavantaj.")
    
    return " ".join(commentary)
