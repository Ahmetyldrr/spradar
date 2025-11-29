"""
1️⃣ COMEBACK POTANSİYELİ ANALİZİ - Comeback Potential Component
=================================================================

Takımın comeback yapma yeteneği, gerideyken kazanma/beraberlik getirme istatistikleri.
Mental güç, mücadele ruhu, vazgeçmeme karakteristiği.
"""

def generate_comeback_potential_commentary(stats):
    """
    Comeback potansiyeli yorumu - YARATICI + ETKİLEŞİMLİ
    
    Args:
        stats: Team istatistikleri dict (team_sum_last_10'dan gelen)
    
    Returns:
        str: Comeback potansiyeli yorumu
    """
    
    matches = int(stats.get('sum_all_matches_played', 0))
    if matches == 0:
        return "Bu takım için yeterli maç verisi yok."
    
    commentary = []
    
    # ==========================================
    # COMEBACK İSTATİSTİKLERİ
    # ==========================================
    comeback_win = int(stats.get('sum_all_sum_comeback_win', 0))
    comeback_draw = int(stats.get('sum_all_sum_comeback_draw', 0))
    
    commentary.append(f"Benim son {matches} maçımda comeback istatistiklerime bakalım.")
    
    if comeback_win > 0:
        comeback_win_rate = comeback_win / matches * 100
        commentary.append(f"Ben {comeback_win} maçta gerideyken geri gelip maçı kazandım (yüzde {comeback_win_rate:.1f}).")
        
        if comeback_win_rate >= 25:
            commentary.append("Bu çok yüksek bir comeback başarısı, ben vazgeçmeyen bir takımım ve geride olsam bile mücadeleyi bırakmıyorum, rakipler beni asla bitmiş sanmamalı.")
        elif comeback_win_rate >= 15:
            commentary.append("Gerideyken sık sık geri gelip kazanabiliyorum, mental gücüm yüksek ve ikinci yarıda çok tehlikeliyim.")
        elif comeback_win_rate >= 5:
            commentary.append("Zaman zaman gerideyken geri gelip kazanabiliyorum ama bu çok sık olmuyor.")
    else:
        commentary.append("Hiçbir maçta gerideyken geri gelip kazanamadım, bu da mental gücümün zayıf olduğunu gösteriyor.")
    
    if comeback_draw > 0:
        comeback_draw_rate = comeback_draw / matches * 100
        commentary.append(f"Ayrıca {comeback_draw} maçta gerideyken geri gelip beraberliği yakaladım (yüzde {comeback_draw_rate:.1f}).")
        
        if comeback_draw_rate >= 20:
            commentary.append("En azından geride olduğumda berabere getirmeyi çok sık başarıyorum, son dakikalarda puan kurtarmayı biliyorum.")
    
    # TOPLAM COMEBACK ORANI
    total_comeback = comeback_win + comeback_draw
    if total_comeback > 0:
        total_comeback_rate = total_comeback / matches * 100
        commentary.append(f"Toplamda {total_comeback} maçta gerideyken geri geldim (yüzde {total_comeback_rate:.1f}), bu benim comeback karakterimi gösteriyor.")
        
        if total_comeback_rate >= 30:
            commentary.append("Neredeyse maçlarımın üçte birinde gerideyken geri geliyorum, bu inanılmaz bir mücadele ruhu ve asla pes etmeme karakteri.")
    else:
        commentary.append("Hiçbir maçta gerideyken geri gelemedim, geride kaldığımda maçı kaybetmeye mahkumum gibi görünüyorum.")
    
    # ==========================================
    # İLK YARI GERİDE KALMA DURUMLARI
    # ==========================================
    ht_loss = int(stats.get('sum_all_sum_ht_loss', 0))
    
    if ht_loss > 0:
        ht_loss_rate = ht_loss / matches * 100
        commentary.append(f"İlk yarıyı geride bitirdiğim {ht_loss} maçta ({ht_loss_rate:.1f}%) ne oldu?")
        
        if total_comeback > 0 and ht_loss > 0:
            # İlk yarı geride → Sonuç comeback
            comeback_from_ht_loss_rate = (total_comeback / ht_loss) * 100 if ht_loss > 0 else 0
            commentary.append(f"İlk yarıyı geride bitirdiğim maçların yüzde {comeback_from_ht_loss_rate:.1f}'inde geri geldim.")
            
            if comeback_from_ht_loss_rate >= 50:
                commentary.append("İlk yarı geride olsam bile yarısından fazlasında geri geliyorum, bu inanılmaz bir ikinci yarı performansı ve mental güç!")
            elif comeback_from_ht_loss_rate >= 30:
                commentary.append("İlk yarı geride olduğumda üçte birinden fazlasında geri gelebiliyorum, soyunma odasında iyi konuşmalar yapıyoruz.")
    
    # ==========================================
    # MOMENTUM DEĞİŞİMİ
    # ==========================================
    momentum_gained = int(stats.get('sum_all_sum_momentum_gained', 0))
    momentum_lost = int(stats.get('sum_all_sum_momentum_lost', 0))
    
    if momentum_gained > 0:
        commentary.append(f"Ben {momentum_gained} maçta momentum kazandım, yani maçın kontrolünü ele geçirdim ve rakibi baskı altına aldım.")
    
    if momentum_lost > 0:
        commentary.append(f"Ama {momentum_lost} maçta momentum kaybettim, yani maçın kontrolünü rakibe kaptırdım ve baskı altına girdim.")
    
    if momentum_gained > momentum_lost * 1.5:
        commentary.append("Momentum istatistiklerim çok iyi, genellikle maçın kontrolünü elime alıyorum ve rakibi baskı altında tutuyorum.")
    elif momentum_lost > momentum_gained * 1.5:
        commentary.append("Momentum istatistiklerim kötü, çok sık maçın kontrolünü kaybediyorum ve rakipler bana hükmedebiliyor.")
    
    return " ".join(commentary)
