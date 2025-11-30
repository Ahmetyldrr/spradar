"""
🎯 COMMENTARY MODULE - RAG SİSTEMİ İÇİN TAKIM YORUM OLUŞTURUCU
============================================================

286 sütunlu team_sum_last_10 tablosu için yapay zeka RAG sistemi

Modules:
    - comprehensive_commentary: 9 komponent kullanarak kapsamlı yorum oluşturma
    - components: 9 modüler komponent (kimlik, maç sonuçları, gol, yarı, vs.)
    - daily_matches: Günlük maç yorumları otomatik oluşturma

Author: Spradar Analytics Team
Date: November 5, 2025
Version: 3.0 - Comprehensive Modular Commentary (286 columns)
"""

from .comprehensive_commentary import (
    generate_comprehensive_natural_commentary,
    generate_match_commentary_comprehensive
)
from .daily_matches import (
    process_daily_matches,
    get_daily_matches,
    generate_match_commentary_with_info,
    save_commentary_to_db,
    get_match_commentary_from_db,
    clear_daily_commentaries_table,
    search_commentaries_by_date,
    search_commentaries_by_team
)

__all__ = [
    'generate_comprehensive_natural_commentary',
    'generate_match_commentary_comprehensive',
    'process_daily_matches',
    'get_daily_matches',
    'generate_match_commentary_with_info',
    'save_commentary_to_db',
    'get_match_commentary_from_db',
    'clear_daily_commentaries_table',
    'search_commentaries_by_date',
    'search_commentaries_by_team'
]

__version__ = '3.0.0'
