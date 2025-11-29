"""
📦 Commentary Components Package
=================================

9 komponent modülünü içeren alt paket.
"""

from .identity_info import generate_identity_commentary
from .match_results import generate_match_results_commentary
from .goal_scoring import generate_goal_scoring_commentary
from .goal_conceding import generate_goal_conceding_commentary
from .first_half_detailed import generate_first_half_detailed_commentary
from .second_half_detailed import generate_second_half_detailed_commentary
from .special_stats import generate_special_stats_commentary
from .high_scoring_goal_diff import generate_high_scoring_goal_diff_commentary
from .home_away_other import generate_home_away_other_commentary

__all__ = [
    'generate_identity_commentary',
    'generate_match_results_commentary',
    'generate_goal_scoring_commentary',
    'generate_goal_conceding_commentary',
    'generate_first_half_detailed_commentary',
    'generate_second_half_detailed_commentary',
    'generate_special_stats_commentary',
    'generate_high_scoring_goal_diff_commentary',
    'generate_home_away_other_commentary'
]
