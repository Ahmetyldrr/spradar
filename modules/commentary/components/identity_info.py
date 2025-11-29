"""
1️⃣ KİMLİK VE GENEL BİLGİLER - Identity Info Component
=====================================================

Takımın temel kimlik bilgileri ve genel performans değerlendirmesi.
"""

def generate_identity_commentary(row):
    """Kimlik bilgilerini yorum olarak oluştur"""
    
    team_name = row.get('team_name', 'Bilinmeyen')
    team_id = row['team_id']
    matches = int(row['sum_all_matches_played'])
    league = row.get('sum_all_tournament_name', 'Bilinmeyen Lig')
    country = row.get('sum_all_country_name', 'Bilinmeyen')
    
    if matches == 0:
        return f"{team_name} - Yeterli maç verisi yok."
    
    # Kısa ve net format
    return f"{team_name} (ID: {team_id}) - {matches} maç / {country} - {league}"
