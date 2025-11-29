"""
3️⃣ İKİNCİ YARI COMEBACK ANALİZİ - Second Half Comeback Component
===================================================================

İkinci yarı performansı ve comeback başarısı.
İkinci yarıda patlama, çöküş, maç sonu dramları.
"""

def generate_second_half_comeback_commentary(stats):
    """
    İkinci yarı comeback yorumu - ETKİLEŞİMLİ + DRAMATIK
    
    Args:
        stats: Team istatistikleri dict
    
    Returns:
        str: İkinci yarı comeback yorumu
    """
    
    matches = int(stats.get('sum_all_matches_played', 0))
    if matches == 0:
        return ""
    
    commentary = []
    
    commentary.append("İkinci yarı performansım comeback için çok kritik, bakalım ne kadar güçlüyüm.")
    
    # ==========================================
    # İKİNCİ YARI GOL ÜRETİMİ
    # ==========================================
    ht2_team_score = float(stats.get('sum_all_sum_team_score_2h', 0))
    ht2_avg_team = float(stats.get('sum_all_avg_team_score_2h', 0))
    ht_avg_team = float(stats.get('sum_all_avg_team_score_1h', 0))
    
    commentary.append(f"İkinci yarılarda toplam {int(ht2_team_score)} gol attım, maç başına ortalama {ht2_avg_team:.2f} gol.")
    
    # İlk yarı vs İkinci yarı gol karşılaştırması
    if ht_avg_team > 0:  # Sıfıra bölme hatası önleme
        if ht2_avg_team > ht_avg_team * 1.3:
            commentary.append(f"İkinci yarılarda ilk yarıya göre yüzde {((ht2_avg_team/ht_avg_team - 1) * 100):.1f} daha fazla gol atıyorum, bu da ikinci yarıda patladığımı gösteriyor!")
            commentary.append("Maç ilerledikçe açılıyorum, rakipler yoruluyor ve ben son 45 dakikada çok daha tehlikeliyim, comeback için ideal bir profil!")
        elif ht2_avg_team < ht_avg_team * 0.7:
            commentary.append(f"İkinci yarılarda ilk yarıya göre yüzde {((1 - ht2_avg_team/ht_avg_team) * 100):.1f} daha az gol atıyorum, bu kötü bir durum.")
            commentary.append("Maç ilerledikçe yoruluyorum veya kapanıyorum, ikinci yarıda etkisiz kalıyorum, comeback yapmam çok zor.")
    
    # ==========================================
    # İKİNCİ YARI GOL DAGILIMI
    # ==========================================
    ht2_team_2plus = int(stats.get('sum_all_sum_ht2_team_gol_sayisi_2', 0))
    ht2_team_3plus = int(stats.get('sum_all_sum_ht2_team_gol_sayisi_3plus', 0))
    
    if ht2_team_2plus > 0:
        ht2_2plus_rate = ht2_team_2plus / matches * 100
        commentary.append(f"İkinci yarıda {ht2_team_2plus} maçta 2 veya daha fazla gol attım (yüzde {ht2_2plus_rate:.1f}).")
        
        if ht2_2plus_rate >= 30:
            commentary.append("İkinci yarılarda sık sık 2+ gol atıyorum, bu inanılmaz bir patlama gücü! Geride olsam bile son 45 dakikada maçı çevirebilirim.")
    
    if ht2_team_3plus > 0:
        commentary.append(f"Hatta {ht2_team_3plus} maçta ikinci yarıda 3 veya daha fazla gol attım, bu bir gol şov!")
    
    # ==========================================
    # İKİNCİ YARI SONUÇLAR
    # ==========================================
    ht2_win = int(stats.get('sum_all_sum_ht2_win', 0))
    ht2_draw = int(stats.get('sum_all_sum_ht2_draw', 0))
    ht2_loss = int(stats.get('sum_all_sum_ht2_loss', 0))
    
    commentary.append(f"İkinci yarı sonuçlarıma bakarsak {ht2_win} maçta kazandım, {ht2_draw} maçta berabere bitirdim, {ht2_loss} maçta kaybettim.")
    
    if ht2_win > 0:
        ht2_win_rate = ht2_win / matches * 100
        commentary.append(f"İkinci yarıda yüzde {ht2_win_rate:.1f} oranında kazandım.")
        
        if ht2_win_rate >= 60:
            commentary.append("İkinci yarılarda çok dominant bir performans gösteriyorum, maçların çoğunu son 45 dakikada kazanıyorum!")
    
    # ==========================================
    # EXPLODED 2H (İKİNCİ YARIDE PATLAMA)
    # ==========================================
    exploded_2h = int(stats.get('sum_all_sum_exploded_2h', 0))
    
    if exploded_2h > 0:
        exploded_rate = exploded_2h / matches * 100
        commentary.append(f"Ben {exploded_2h} maçta ikinci yarıda patladım (yüzde {exploded_rate:.1f}), yani son 45 dakikada çok fazla gol attım ve rakibi ezdim!")
        
        if exploded_rate >= 25:
            commentary.append("Sık sık ikinci yarıda patlıyorum, bu da rakiplerin beni son dakikalarda durduramadığını gösteriyor, geride olsam bile her zaman umut var!")
    
    # ==========================================
    # COLLAPSED 2H (İKİNCİ YARIDE ÇÖKÜŞ)
    # ==========================================
    collapsed_2h = int(stats.get('sum_all_sum_collapsed_2h', 0))
    
    if collapsed_2h > 0:
        collapsed_rate = collapsed_2h / matches * 100
        commentary.append(f"Ama dikkat! {collapsed_2h} maçta ikinci yarıda çöktüm (yüzde {collapsed_rate:.1f}), yani son 45 dakikada çok fazla gol yedim ve maçı kaybettim.")
        
        if collapsed_rate >= 25:
            commentary.append("Sık sık ikinci yarıda çöküyorum, bu da maç ilerledikçe yorulduğumu ve rakiplerin beni son dakikalarda ezdiğini gösteriyor, bu benim için çok tehlikeli!")
    
    # ==========================================
    # MORE GOALS 2H (İKİNCİ YARIDE DAHA FAZLA GOL)
    # ==========================================
    more_goals_2h = int(stats.get('sum_all_sum_more_goals_2h', 0))
    
    if more_goals_2h > 0:
        more_goals_rate = more_goals_2h / matches * 100
        commentary.append(f"Ben {more_goals_2h} maçta ikinci yarıda ilk yarıya göre daha fazla gol attım (yüzde {more_goals_rate:.1f}).")
        
        if more_goals_rate >= 50:
            commentary.append("Maçların yarısından fazlasında ikinci yarıda daha fazla gol atıyorum, bu da maç ilerledikçe açıldığımı gösteriyor!")
    
    # ==========================================
    # İKİNCİ YARI CLEAN SHEET
    # ==========================================
    ht2_clean_sheet = int(stats.get('sum_all_sum_ht2_team_clean_sheet', 0))
    
    if ht2_clean_sheet > 0:
        ht2_cs_rate = ht2_clean_sheet / matches * 100
        commentary.append(f"İkinci yarıda {ht2_clean_sheet} maçta gol yemedim (yüzde {ht2_cs_rate:.1f}), bu da son 45 dakikayı iyi kilitlediğimi gösteriyor.")
    
    # ==========================================
    # İKİNCİ YARI SCORED BOTH HALVES
    # ==========================================
    scored_both_halves = int(stats.get('sum_all_sum_scored_both_halves', 0))
    
    if scored_both_halves > 0:
        both_rate = scored_both_halves / matches * 100
        commentary.append(f"Ben {scored_both_halves} maçta hem ilk yarıda hem ikinci yarıda gol attım (yüzde {both_rate:.1f}), bu da her iki yarıda da tehlikeli olduğumu gösteriyor.")
    
    return " ".join(commentary)
