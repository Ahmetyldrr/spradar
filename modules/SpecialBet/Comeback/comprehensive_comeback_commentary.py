"""
🎯 COMPREHENSIVE COMEBACK COMMENTARY GENERATOR
===============================================

Tüm comeback bileşenlerini birleştirerek kapsamlı analiz oluşturur.
AI için optimize edilmiş, doğal dil formatında commentary.
"""

import sys
sys.path.append('/home/ahmet/Desktop/Spradar1')

from modules.SpecialBet.Comeback.components.comeback_potential import generate_comeback_potential_commentary
from modules.SpecialBet.Comeback.components.first_half_comeback import generate_first_half_comeback_commentary
from modules.SpecialBet.Comeback.components.second_half_comeback import generate_second_half_comeback_commentary
from modules.SpecialBet.Comeback.components.momentum_analysis import generate_momentum_analysis_commentary
from modules.SpecialBet.Comeback.components.lead_management import generate_lead_management_commentary
from modules.SpecialBet.Comeback.components.match_interaction import generate_match_interaction_commentary


def generate_comprehensive_comeback_commentary(home_stats, away_stats, match_info):
    """
    Kapsamlı comeback commentary'si oluştur
    
    Args:
        home_stats: Ev sahibi istatistikleri dict (team_sum_last_10)
        away_stats: Deplasman istatistikleri dict (team_sum_last_10)
        match_info: Maç bilgileri dict
    
    Returns:
        dict: {
            'combined_prompt': str - Tüm commentary birleştirilmiş,
            'home_commentary': dict - Ev sahibi bileşenler,
            'away_commentary': dict - Deplasman bileşenler,
            'interaction_analysis': str - Etkileşim analizi,
            'ai_question': str - AI sorusu,
            'metadata': dict - Meta bilgiler
        }
    """
    
    # ==========================================
    # EV SAHİBİ COMMENTARY
    # ==========================================
    home_team_name = match_info.get('home_team_name', 'Ev Sahibi')
    
    home_commentary = {
        'team_name': home_team_name,
        'comeback_potential': generate_comeback_potential_commentary(home_stats),
        'first_half_comeback': generate_first_half_comeback_commentary(home_stats),
        'second_half_comeback': generate_second_half_comeback_commentary(home_stats),
        'momentum_analysis': generate_momentum_analysis_commentary(home_stats),
        'lead_management': generate_lead_management_commentary(home_stats)
    }
    
    # ==========================================
    # DEPLASMAN COMMENTARY
    # ==========================================
    away_team_name = match_info.get('away_team_name', 'Deplasman')
    
    away_commentary = {
        'team_name': away_team_name,
        'comeback_potential': generate_comeback_potential_commentary(away_stats),
        'first_half_comeback': generate_first_half_comeback_commentary(away_stats),
        'second_half_comeback': generate_second_half_comeback_commentary(away_stats),
        'momentum_analysis': generate_momentum_analysis_commentary(away_stats),
        'lead_management': generate_lead_management_commentary(away_stats)
    }
    
    # ==========================================
    # ETKİLEŞİM ANALİZİ
    # ==========================================
    home_interaction = generate_match_interaction_commentary(home_stats, away_stats, team_type='home')
    away_interaction = generate_match_interaction_commentary(home_stats, away_stats, team_type='away')
    
    # ==========================================
    # KOMBİNE PROMPT OLUŞTUR
    # ==========================================
    combined_prompt = f"""
{'='*80}
🏆 COMEBACK ANALİZİ: {home_team_name} vs {away_team_name}
{'='*80}

📅 Tarih: {match_info.get('match_date', 'N/A')}
⏰ Saat: {match_info.get('match_time', 'N/A')}
🏟️ Lig: {match_info.get('league', 'N/A')}
🌍 Ülke: {match_info.get('country', 'N/A')}

{'='*80}
🏠 EV SAHİBİ: {home_team_name}
{'='*80}

📊 COMEBACK POTANSİYELİ:
{home_commentary['comeback_potential']}

⏱️ İLK YARI COMEBACK ANALİZİ:
{home_commentary['first_half_comeback']}

⏱️ İKİNCİ YARI COMEBACK ANALİZİ:
{home_commentary['second_half_comeback']}

💪 MOMENTUM ANALİZİ:
{home_commentary['momentum_analysis']}

🛡️ AVANTAJ YÖNETİMİ:
{home_commentary['lead_management']}

{'='*80}
✈️ DEPLASMAN: {away_team_name}
{'='*80}

📊 COMEBACK POTANSİYELİ:
{away_commentary['comeback_potential']}

⏱️ İLK YARI COMEBACK ANALİZİ:
{away_commentary['first_half_comeback']}

⏱️ İKİNCİ YARI COMEBACK ANALİZİ:
{away_commentary['second_half_comeback']}

💪 MOMENTUM ANALİZİ:
{away_commentary['momentum_analysis']}

🛡️ AVANTAJ YÖNETİMİ:
{away_commentary['lead_management']}

{'='*80}
🔄 MAÇ ETKİLEŞİM ANALİZİ
{'='*80}

🏠 EV SAHİBİ PERSPEKTİFİ:
{home_interaction}

✈️ DEPLASMAN PERSPEKTİFİ:
{away_interaction}

{'='*80}
🤖 AI SORUSU
{'='*80}

Bu maçta COMEBACK (geriden dönüş) olma ihtimali var mı? 
Hangi takımın comeback yapma şansı daha yüksek?
İlk yarı ve ikinci yarı performanslarına göre detaylı analiz yap.
İki takımın etkileşimini değerlendir: İlk yarı kötü oynayan bir takım ilk yarı iyi oynayan 
bir takımla karşılaşırsa ne olur? İlk yarı iyi oynayan takım ikinci yarı kötü oynuyor olabilir mi?
Comeback olasılığı yüzde kaç? Hangi senaryolar mümkün?

{'='*80}
"""
    
    # ==========================================
    # METADATA
    # ==========================================
    metadata = {
        'home_team_id': match_info.get('home_team_id'),
        'away_team_id': match_info.get('away_team_id'),
        'match_id': match_info.get('match_id'),
        'season_id': match_info.get('season_id'),
        'home_matches_analyzed': int(home_stats.get('sum_all_matches_played', 0)),
        'away_matches_analyzed': int(away_stats.get('sum_all_matches_played', 0)),
        'home_comeback_win': int(home_stats.get('sum_all_sum_comeback_win', 0)),
        'away_comeback_win': int(away_stats.get('sum_all_sum_comeback_win', 0)),
        'home_lead_lost': int(home_stats.get('sum_all_sum_lead_lost', 0)),
        'away_lead_lost': int(away_stats.get('sum_all_sum_lead_lost', 0))
    }
    
    return {
        'combined_prompt': combined_prompt.strip(),
        'home_commentary': home_commentary,
        'away_commentary': away_commentary,
        'interaction_analysis': {
            'home_perspective': home_interaction,
            'away_perspective': away_interaction
        },
        'ai_question': "Bu maçta COMEBACK (geriden dönüş) olma ihtimali var mı? Hangi takımın comeback yapma şansı daha yüksek? İlk yarı ve ikinci yarı performanslarına göre detaylı analiz yap. İki takımın etkileşimini değerlendir. Comeback olasılığı yüzde kaç?",
        'metadata': metadata
    }


if __name__ == "__main__":
    print("✅ Comprehensive Comeback Commentary Generator hazır!")
    print("📦 Tüm bileşenler yüklendi:")
    print("   1️⃣ Comeback Potential")
    print("   2️⃣ First Half Comeback")
    print("   3️⃣ Second Half Comeback")
    print("   4️⃣ Momentum Analysis")
    print("   5️⃣ Lead Management")
    print("   6️⃣ Match Interaction")
