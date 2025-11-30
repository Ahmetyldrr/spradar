"""
💬 COMEBACK COMMENTARY GENERATOR
================================

Comeback analizi sonuçlarını AI için prompt formatına dönüştürür
"""

import json


def generate_comeback_commentary_json(match_data, home_analysis, away_analysis):
    """
    Comeback analizi verilerinden AI için JSON prompt oluştur
    
    Args:
        match_data: Maç bilgileri dict
        home_analysis: Ev sahibi comeback analizi
        away_analysis: Deplasman comeback analizi
    
    Returns:
        dict: JSON formatında comeback analizi
    """
    
    return {
        "mac_bilgileri": {
            "tarih": match_data.get('match_date', 'N/A'),
            "saat": match_data.get('match_time', 'N/A'),
            "lig": match_data.get('league', 'N/A'),
            "ulke": match_data.get('country', 'N/A'),
            "ev_sahibi": match_data.get('home_team_name', 'N/A'),
            "deplasman": match_data.get('away_team_name', 'N/A')
        },
        "ev_sahibi_analizi": {
            "toplam_mac": home_analysis['total_matches'],
            "comeback_potansiyeli": {
                "comeback_kazanma": f"{home_analysis['comeback_win_count']} maç ({home_analysis['comeback_win_pct']}%)",
                "comeback_beraberlik": f"{home_analysis['comeback_draw_count']} maç ({home_analysis['comeback_draw_pct']}%)",
                "once_onde_sonra_kaybetti": f"{home_analysis['lead_lost_count']} maç ({home_analysis['lead_lost_pct']}%)",
                "comeback_skor": f"{home_analysis['comeback_potential_score']}/100",
                "lead_lost_risk": f"{home_analysis['lead_lost_risk_score']}/100"
            },
            "ilk_yari": {
                "kazandi": f"{home_analysis['ht_win_count']} ({home_analysis['ht_win_pct']}%)",
                "berabere": f"{home_analysis['ht_draw_count']} ({home_analysis['ht_draw_pct']}%)",
                "kaybetti": f"{home_analysis['ht_loss_count']} ({home_analysis['ht_loss_pct']}%)",
                "ort_attigi_gol": home_analysis['avg_ht_scored'],
                "ort_yedigi_gol": home_analysis['avg_ht_conceded'],
                "clean_sheet_yuzde": home_analysis['ht_clean_sheet_pct'],
                "over_05_yuzde": home_analysis['ht_over_05_pct'],
                "over_15_yuzde": home_analysis['ht_over_15_pct']
            },
            "ikinci_yari": {
                "kazandi": f"{home_analysis['ht2_win_count']} ({home_analysis['ht2_win_pct']}%)",
                "berabere": f"{home_analysis['ht2_draw_count']} ({home_analysis['ht2_draw_pct']}%)",
                "kaybetti": f"{home_analysis['ht2_loss_count']} ({home_analysis['ht2_loss_pct']}%)",
                "ort_attigi_gol": home_analysis['avg_ht2_scored'],
                "ort_yedigi_gol": home_analysis['avg_ht2_conceded'],
                "clean_sheet_yuzde": home_analysis['ht2_clean_sheet_pct'],
                "over_05_yuzde": home_analysis['ht2_over_05_pct'],
                "over_15_yuzde": home_analysis['ht2_over_15_pct']
            },
            "gol_dagilimi_ilk_yari": {
                "0_gol": home_analysis['ht_team_0_gol'],
                "1_gol": home_analysis['ht_team_1_gol'],
                "2_gol": home_analysis['ht_team_2_gol'],
                "3plus_gol": home_analysis['ht_team_3plus_gol']
            },
            "gol_dagilimi_ikinci_yari": {
                "0_gol": home_analysis['ht2_team_0_gol'],
                "1_gol": home_analysis['ht2_team_1_gol'],
                "2_gol": home_analysis['ht2_team_2_gol'],
                "3plus_gol": home_analysis['ht2_team_3plus_gol']
            }
        },
        "deplasman_analizi": {
            "toplam_mac": away_analysis['total_matches'],
            "comeback_potansiyeli": {
                "comeback_kazanma": f"{away_analysis['comeback_win_count']} maç ({away_analysis['comeback_win_pct']}%)",
                "comeback_beraberlik": f"{away_analysis['comeback_draw_count']} maç ({away_analysis['comeback_draw_pct']}%)",
                "once_onde_sonra_kaybetti": f"{away_analysis['lead_lost_count']} maç ({away_analysis['lead_lost_pct']}%)",
                "comeback_skor": f"{away_analysis['comeback_potential_score']}/100",
                "lead_lost_risk": f"{away_analysis['lead_lost_risk_score']}/100"
            },
            "ilk_yari": {
                "kazandi": f"{away_analysis['ht_win_count']} ({away_analysis['ht_win_pct']}%)",
                "berabere": f"{away_analysis['ht_draw_count']} ({away_analysis['ht_draw_pct']}%)",
                "kaybetti": f"{away_analysis['ht_loss_count']} ({away_analysis['ht_loss_pct']}%)",
                "ort_attigi_gol": away_analysis['avg_ht_scored'],
                "ort_yedigi_gol": away_analysis['avg_ht_conceded'],
                "clean_sheet_yuzde": away_analysis['ht_clean_sheet_pct']
            },
            "ikinci_yari": {
                "kazandi": f"{away_analysis['ht2_win_count']} ({away_analysis['ht2_win_pct']}%)",
                "berabere": f"{away_analysis['ht2_draw_count']} ({away_analysis['ht2_draw_pct']}%)",
                "kaybetti": f"{away_analysis['ht2_loss_count']} ({away_analysis['ht2_loss_pct']}%)",
                "ort_attigi_gol": away_analysis['avg_ht2_scored'],
                "ort_yedigi_gol": away_analysis['avg_ht2_conceded'],
                "clean_sheet_yuzde": away_analysis['ht2_clean_sheet_pct']
            },
            "gol_dagilimi_ilk_yari": {
                "0_gol": away_analysis['ht_team_0_gol'],
                "1_gol": away_analysis['ht_team_1_gol'],
                "2_gol": away_analysis['ht_team_2_gol'],
                "3plus_gol": away_analysis['ht_team_3plus_gol']
            },
            "gol_dagilimi_ikinci_yari": {
                "0_gol": away_analysis['ht2_team_0_gol'],
                "1_gol": away_analysis['ht2_team_1_gol'],
                "2_gol": away_analysis['ht2_team_2_gol'],
                "3plus_gol": away_analysis['ht2_team_3plus_gol']
            }
        },
        "ai_sorusu": "Bu maçta COMEBACK (geriden dönüş) olma ihtimali var mı? Hangi takımın comeback yapma şansı daha yüksek? İlk yarı ve ikinci yarı performanslarına göre detaylı analiz yap. Comeback olasılığı yüzde kaç?"
    }


def generate_comeback_commentary(match_data, home_analysis, away_analysis):
    """
    Comeback analizi verilerinden AI için commentary prompt'u oluştur
    
    Args:
        match_data: Maç bilgileri dict
        home_analysis: Ev sahibi comeback analizi
        away_analysis: Deplasman comeback analizi
    
    Returns:
        str: AI için hazır prompt
    """
    
    commentary = []
    
    # Başlık
    commentary.append("=" * 80)
    commentary.append("🔄 COMEBACK ANALİZİ - DETAYLI RAPOR")
    commentary.append("=" * 80)
    commentary.append("")
    
    # Maç Bilgileri
    commentary.append(f"📅 Tarih: {match_data.get('match_date', 'N/A')}")
    commentary.append(f"⏰ Saat: {match_data.get('match_time', 'N/A')}")
    commentary.append(f"🏆 Lig: {match_data.get('league', 'N/A')}")
    commentary.append(f"🌍 Ülke: {match_data.get('country', 'N/A')}")
    commentary.append("")
    
    commentary.append(f"🏠 EV SAHİBİ: {match_data.get('home_team_name', 'N/A')}")
    commentary.append(f"✈️  DEPLASMAN: {match_data.get('away_team_name', 'N/A')}")
    commentary.append("")
    commentary.append("=" * 80)
    commentary.append("")
    
    # Ev Sahibi Analizi
    commentary.append("🏠 EV SAHİBİ COMEBACK ANALİZİ")
    commentary.append("-" * 80)
    commentary.append(f"📊 Toplam Maç: {home_analysis['total_matches']}")
    commentary.append("")
    
    if home_analysis['total_matches'] > 0:
        commentary.append("🔥 COMEBACK POTANSİYELİ:")
        commentary.append(f"  • Comeback Kazanma: {home_analysis['comeback_win_count']} maç ({home_analysis['comeback_win_pct']}%)")
        commentary.append(f"  • Comeback Beraberlik: {home_analysis['comeback_draw_count']} maç ({home_analysis['comeback_draw_pct']}%)")
        commentary.append(f"  • Önce Öndeydi Kaybetti: {home_analysis['lead_lost_count']} maç ({home_analysis['lead_lost_pct']}%)")
        commentary.append(f"  • 🎯 Comeback Potansiyel Skoru: {home_analysis['comeback_potential_score']}/100")
        commentary.append(f"  • ⚠️  Lead Lost Risk Skoru: {home_analysis['lead_lost_risk_score']}/100")
        commentary.append("")
        
        commentary.append("⏱️  İLK YARI PERFORMANSI:")
        commentary.append(f"  • Kazandı: {home_analysis['ht_win_count']} ({home_analysis['ht_win_pct']}%)")
        commentary.append(f"  • Berabere: {home_analysis['ht_draw_count']} ({home_analysis['ht_draw_pct']}%)")
        commentary.append(f"  • Kaybetti: {home_analysis['ht_loss_count']} ({home_analysis['ht_loss_pct']}%)")
        commentary.append(f"  • Ortalama Attığı Gol: {home_analysis['avg_ht_scored']}")
        commentary.append(f"  • Ortalama Yediği Gol: {home_analysis['avg_ht_conceded']}")
        commentary.append(f"  • Clean Sheet: {home_analysis['ht_clean_sheet']} ({home_analysis['ht_clean_sheet_pct']}%)")
        commentary.append(f"  • Over 0.5: {home_analysis['ht_over_05']} ({home_analysis['ht_over_05_pct']}%)")
        commentary.append(f"  • Over 1.5: {home_analysis['ht_over_15']} ({home_analysis['ht_over_15_pct']}%)")
        commentary.append("")
        
        commentary.append("⏱️  İKİNCİ YARI PERFORMANSI:")
        commentary.append(f"  • Kazandı: {home_analysis['ht2_win_count']} ({home_analysis['ht2_win_pct']}%)")
        commentary.append(f"  • Berabere: {home_analysis['ht2_draw_count']} ({home_analysis['ht2_draw_pct']}%)")
        commentary.append(f"  • Kaybetti: {home_analysis['ht2_loss_count']} ({home_analysis['ht2_loss_pct']}%)")
        commentary.append(f"  • Ortalama Attığı Gol: {home_analysis['avg_ht2_scored']}")
        commentary.append(f"  • Ortalama Yediği Gol: {home_analysis['avg_ht2_conceded']}")
        commentary.append(f"  • Clean Sheet: {home_analysis['ht2_clean_sheet']} ({home_analysis['ht2_clean_sheet_pct']}%)")
        commentary.append(f"  • Over 0.5: {home_analysis['ht2_over_05']} ({home_analysis['ht2_over_05_pct']}%)")
        commentary.append(f"  • Over 1.5: {home_analysis['ht2_over_15']} ({home_analysis['ht2_over_15_pct']}%)")
        commentary.append("")
        
        commentary.append("⚽ GOL DAĞILIMI (İlk Yarı):")
        commentary.append(f"  • 0 Gol: {home_analysis['ht_team_0_gol']} maç")
        commentary.append(f"  • 1 Gol: {home_analysis['ht_team_1_gol']} maç")
        commentary.append(f"  • 2 Gol: {home_analysis['ht_team_2_gol']} maç")
        commentary.append(f"  • 3+ Gol: {home_analysis['ht_team_3plus_gol']} maç")
        commentary.append("")
        
        commentary.append("⚽ GOL DAĞILIMI (İkinci Yarı):")
        commentary.append(f"  • 0 Gol: {home_analysis['ht2_team_0_gol']} maç")
        commentary.append(f"  • 1 Gol: {home_analysis['ht2_team_1_gol']} maç")
        commentary.append(f"  • 2 Gol: {home_analysis['ht2_team_2_gol']} maç")
        commentary.append(f"  • 3+ Gol: {home_analysis['ht2_team_3plus_gol']} maç")
        commentary.append("")
    else:
        commentary.append("⚠️  Veri yok")
        commentary.append("")
    
    commentary.append("=" * 80)
    commentary.append("")
    
    # Deplasman Analizi
    commentary.append("✈️  DEPLASMAN COMEBACK ANALİZİ")
    commentary.append("-" * 80)
    commentary.append(f"📊 Toplam Maç: {away_analysis['total_matches']}")
    commentary.append("")
    
    if away_analysis['total_matches'] > 0:
        commentary.append("🔥 COMEBACK POTANSİYELİ:")
        commentary.append(f"  • Comeback Kazanma: {away_analysis['comeback_win_count']} maç ({away_analysis['comeback_win_pct']}%)")
        commentary.append(f"  • Comeback Beraberlik: {away_analysis['comeback_draw_count']} maç ({away_analysis['comeback_draw_pct']}%)")
        commentary.append(f"  • Önce Öndeydi Kaybetti: {away_analysis['lead_lost_count']} maç ({away_analysis['lead_lost_pct']}%)")
        commentary.append(f"  • 🎯 Comeback Potansiyel Skoru: {away_analysis['comeback_potential_score']}/100")
        commentary.append(f"  • ⚠️  Lead Lost Risk Skoru: {away_analysis['lead_lost_risk_score']}/100")
        commentary.append("")
        
        commentary.append("⏱️  İLK YARI PERFORMANSI:")
        commentary.append(f"  • Kazandı: {away_analysis['ht_win_count']} ({away_analysis['ht_win_pct']}%)")
        commentary.append(f"  • Berabere: {away_analysis['ht_draw_count']} ({away_analysis['ht_draw_pct']}%)")
        commentary.append(f"  • Kaybetti: {away_analysis['ht_loss_count']} ({away_analysis['ht_loss_pct']}%)")
        commentary.append(f"  • Ortalama Attığı Gol: {away_analysis['avg_ht_scored']}")
        commentary.append(f"  • Ortalama Yediği Gol: {away_analysis['avg_ht_conceded']}")
        commentary.append(f"  • Clean Sheet: {away_analysis['ht_clean_sheet']} ({away_analysis['ht_clean_sheet_pct']}%)")
        commentary.append("")
        
        commentary.append("⏱️  İKİNCİ YARI PERFORMANSI:")
        commentary.append(f"  • Kazandı: {away_analysis['ht2_win_count']} ({away_analysis['ht2_win_pct']}%)")
        commentary.append(f"  • Berabere: {away_analysis['ht2_draw_count']} ({away_analysis['ht2_draw_pct']}%)")
        commentary.append(f"  • Kaybetti: {away_analysis['ht2_loss_count']} ({away_analysis['ht2_loss_pct']}%)")
        commentary.append(f"  • Ortalama Attığı Gol: {away_analysis['avg_ht2_scored']}")
        commentary.append(f"  • Ortalama Yediği Gol: {away_analysis['avg_ht2_conceded']}")
        commentary.append("")
        
        commentary.append("⚽ GOL DAĞILIMI (İlk Yarı):")
        commentary.append(f"  • 0 Gol: {away_analysis['ht_team_0_gol']} maç")
        commentary.append(f"  • 1 Gol: {away_analysis['ht_team_1_gol']} maç")
        commentary.append(f"  • 2 Gol: {away_analysis['ht_team_2_gol']} maç")
        commentary.append(f"  • 3+ Gol: {away_analysis['ht_team_3plus_gol']} maç")
        commentary.append("")
        
        commentary.append("⚽ GOL DAĞILIMI (İkinci Yarı):")
        commentary.append(f"  • 0 Gol: {away_analysis['ht2_team_0_gol']} maç")
        commentary.append(f"  • 1 Gol: {away_analysis['ht2_team_1_gol']} maç")
        commentary.append(f"  • 2 Gol: {away_analysis['ht2_team_2_gol']} maç")
        commentary.append(f"  • 3+ Gol: {away_analysis['ht2_team_3plus_gol']} maç")
        commentary.append("")
    else:
        commentary.append("⚠️  Veri yok")
        commentary.append("")
    
    commentary.append("=" * 80)
    commentary.append("")
    
    # Karşılaştırmalı Analiz
    if home_analysis['total_matches'] > 0 and away_analysis['total_matches'] > 0:
        commentary.append("⚖️  KARŞILAŞTIRMALI ANALİZ")
        commentary.append("-" * 80)
        
        # Comeback potansiyeli karşılaştırma
        if home_analysis['comeback_potential_score'] > away_analysis['comeback_potential_score']:
            diff = home_analysis['comeback_potential_score'] - away_analysis['comeback_potential_score']
            commentary.append(f"✅ Ev sahibinin comeback potansiyeli {diff:.1f} puan daha yüksek")
        elif away_analysis['comeback_potential_score'] > home_analysis['comeback_potential_score']:
            diff = away_analysis['comeback_potential_score'] - home_analysis['comeback_potential_score']
            commentary.append(f"✅ Deplasmanın comeback potansiyeli {diff:.1f} puan daha yüksek")
        else:
            commentary.append(f"⚖️  Her iki takımın da comeback potansiyeli eşit")
        
        commentary.append("")
        
        # İkinci yarı performansı
        if home_analysis['ht2_win_pct'] > away_analysis['ht2_win_pct']:
            diff = home_analysis['ht2_win_pct'] - away_analysis['ht2_win_pct']
            commentary.append(f"💪 Ev sahibi ikinci yarıda %{diff:.1f} daha fazla kazanıyor")
        elif away_analysis['ht2_win_pct'] > home_analysis['ht2_win_pct']:
            diff = away_analysis['ht2_win_pct'] - home_analysis['ht2_win_pct']
            commentary.append(f"💪 Deplasman ikinci yarıda %{diff:.1f} daha fazla kazanıyor")
        
        commentary.append("")
        commentary.append("=" * 80)
    
    return "\n".join(commentary)
