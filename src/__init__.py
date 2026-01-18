"""
Transfer Portal Dashboard - Source Package

Modules:
- theme: UI styling and CSS
- data: Team and player data management
- valuation: Player value calculation methodology
- news_feed: Live news aggregation
- scraper: Web scraping utilities
"""

from .theme import get_custom_css, COLORS
from .data import get_team_data, get_team_details, get_all_teams_list
from .valuation import calculate_player_value
from .news_feed import get_latest_news
