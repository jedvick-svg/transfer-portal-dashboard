"""
Transfer Portal Data Scraper

This module handles fetching transfer portal data from various sources:
- 247Sports Transfer Portal (player transfers, ratings, status)
- 247Sports Recruit Rankings (high school recruit ratings by year)
- ESPN College Football Stats (player performance stats)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional, List, Dict
import time
import re


class TransferPortalScraper:
    """Scraper for college football transfer portal data."""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_247_transfer_portal(self, year: int = 2025, max_pages: int = 5) -> pd.DataFrame:
        """
        Fetch transfer portal data from 247Sports.

        Data includes: player name, rating, position, height/weight,
        status (Committed/Available/Withdrawn), source school, destination school

        Args:
            year: The recruiting year (e.g., 2025)
            max_pages: Maximum number of pages to scrape (25 players per page)

        Returns:
            DataFrame with transfer portal entries
        """
        base_url = f"https://247sports.com/Season/{year}-Football/TransferPortal/"
        all_players = []

        for page in range(1, max_pages + 1):
            try:
                url = f"{base_url}?page={page}" if page > 1 else base_url
                response = self.session.get(url, timeout=10)

                if response.status_code != 200:
                    print(f"Failed to fetch page {page}: {response.status_code}")
                    break

                soup = BeautifulSoup(response.text, 'lxml')

                # Find player entries - adjust selectors based on actual page structure
                player_rows = soup.select('.transfer-portal-row, .player-row, li.rankings-page__list-item')

                for row in player_rows:
                    player = self._parse_247_player(row)
                    if player:
                        all_players.append(player)

                # Be respectful - don't hammer the server
                time.sleep(1)

            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break

        return pd.DataFrame(all_players)

    def _parse_247_player(self, row) -> Optional[Dict]:
        """Parse a single player row from 247Sports."""
        try:
            # Extract player info - selectors may need adjustment
            name_elem = row.select_one('.name, .player-name, a.rankings-page__name-link')
            rating_elem = row.select_one('.rating, .score, .rankings-page__star-and-score')
            position_elem = row.select_one('.position, .pos')
            status_elem = row.select_one('.status, .transfer-status')

            player = {
                'name': name_elem.get_text(strip=True) if name_elem else None,
                'rating': self._extract_rating(rating_elem),
                'position': position_elem.get_text(strip=True) if position_elem else None,
                'status': status_elem.get_text(strip=True) if status_elem else None,
                'source': '247Sports'
            }

            # Only return if we got at least a name
            return player if player['name'] else None

        except Exception as e:
            return None

    def _extract_rating(self, elem) -> Optional[float]:
        """Extract numeric rating from element."""
        if not elem:
            return None
        text = elem.get_text(strip=True)
        # Look for decimal ratings like 0.9842 or 94.2
        match = re.search(r'(\d+\.?\d*)', text)
        return float(match.group(1)) if match else None

    def get_247_recruit_rankings(self, year: int = 2027, max_pages: int = 5) -> pd.DataFrame:
        """
        Fetch high school recruit rankings from 247Sports.

        Use this to get historical ratings for players who later entered the portal.

        Args:
            year: The recruiting class year
            max_pages: Maximum pages to fetch

        Returns:
            DataFrame with recruit rankings
        """
        base_url = f"https://247sports.com/season/{year}-football/recruitrankings/"
        all_recruits = []

        for page in range(1, max_pages + 1):
            try:
                url = f"{base_url}?page={page}" if page > 1 else base_url
                response = self.session.get(url, timeout=10)

                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, 'lxml')

                # Parse recruit rows
                recruit_rows = soup.select('li.rankings-page__list-item')

                for row in recruit_rows:
                    recruit = self._parse_recruit(row)
                    if recruit:
                        all_recruits.append(recruit)

                time.sleep(1)

            except Exception as e:
                print(f"Error fetching recruits page {page}: {e}")
                break

        return pd.DataFrame(all_recruits)

    def _parse_recruit(self, row) -> Optional[Dict]:
        """Parse a single recruit row."""
        try:
            name_elem = row.select_one('.rankings-page__name-link')
            rating_elem = row.select_one('.rankings-page__star-and-score')
            position_elem = row.select_one('.position')
            school_elem = row.select_one('.rankings-page__school')
            commit_elem = row.select_one('.rankings-page__commitment')

            return {
                'name': name_elem.get_text(strip=True) if name_elem else None,
                'rating': self._extract_rating(rating_elem),
                'position': position_elem.get_text(strip=True) if position_elem else None,
                'high_school': school_elem.get_text(strip=True) if school_elem else None,
                'committed_to': commit_elem.get_text(strip=True) if commit_elem else None,
                'source': '247Sports'
            }
        except Exception:
            return None

    def get_espn_stats(self, year: int = 2025, stat_type: str = 'passing') -> pd.DataFrame:
        """
        Fetch player stats from ESPN.

        Args:
            year: Season year
            stat_type: One of 'passing', 'rushing', 'receiving', 'tackles', 'sacks', 'interceptions'

        Returns:
            DataFrame with player stats
        """
        stat_urls = {
            'passing': f'https://www.espn.com/college-football/stats/player/_/stat/passing/season/{year}/seasontype/2',
            'rushing': f'https://www.espn.com/college-football/stats/player/_/stat/rushing/season/{year}/seasontype/2',
            'receiving': f'https://www.espn.com/college-football/stats/player/_/stat/receiving/season/{year}/seasontype/2',
            'tackles': f'https://www.espn.com/college-football/stats/player/_/stat/tackles/season/{year}/seasontype/2',
            'sacks': f'https://www.espn.com/college-football/stats/player/_/stat/sacks/season/{year}/seasontype/2',
            'interceptions': f'https://www.espn.com/college-football/stats/player/_/stat/interceptions/season/{year}/seasontype/2',
        }

        url = stat_urls.get(stat_type)
        if not url:
            return pd.DataFrame()

        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')

            # ESPN uses tables for stats
            tables = soup.select('table')

            players = []
            # Parse table rows - ESPN structure varies, may need adjustment
            for table in tables:
                rows = table.select('tr')
                for row in rows[1:]:  # Skip header
                    cells = row.select('td')
                    if len(cells) >= 2:
                        players.append({
                            'name': cells[0].get_text(strip=True),
                            'team': cells[1].get_text(strip=True) if len(cells) > 1 else None,
                            'stat_value': cells[2].get_text(strip=True) if len(cells) > 2 else None,
                            'stat_type': stat_type,
                            'year': year,
                            'source': 'ESPN'
                        })

            return pd.DataFrame(players)

        except Exception as e:
            print(f"Error fetching ESPN stats: {e}")
            return pd.DataFrame()


def calculate_team_rankings(transfers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate team rankings based on transfer portal activity.

    Ranks teams by:
    - Number of transfers acquired
    - Average rating of acquired transfers
    - Total "value" (sum of ratings)

    Args:
        transfers_df: DataFrame with transfer portal data

    Returns:
        DataFrame with team rankings
    """
    if transfers_df.empty:
        return pd.DataFrame()

    # Filter to committed/enrolled players with a destination
    committed = transfers_df[
        transfers_df['status'].str.contains('Committed|Enrolled', case=False, na=False)
    ]

    # Group by destination team
    team_stats = committed.groupby('destination').agg({
        'name': 'count',
        'rating': ['mean', 'sum']
    }).reset_index()

    team_stats.columns = ['Team', 'Transfers', 'Avg_Rating', 'Total_Rating']

    # Calculate composite score for ranking
    team_stats['Score'] = (
        team_stats['Transfers'] * 0.3 +
        team_stats['Avg_Rating'] * 0.4 +
        team_stats['Total_Rating'] * 0.3
    )

    # Rank teams
    team_stats = team_stats.sort_values('Score', ascending=False).reset_index(drop=True)
    team_stats['Rank'] = range(1, len(team_stats) + 1)

    return team_stats[['Rank', 'Team', 'Transfers', 'Avg_Rating', 'Total_Rating', 'Score']]


# Convenience function for quick data fetch
def fetch_all_data(year: int = 2025) -> Dict[str, pd.DataFrame]:
    """
    Fetch all available data for a given year.

    Returns dict with keys: 'transfers', 'recruits', 'passing', 'rushing', etc.
    """
    scraper = TransferPortalScraper()

    data = {
        'transfers': scraper.get_247_transfer_portal(year=year),
        'recruits': scraper.get_247_recruit_rankings(year=year),
        'passing': scraper.get_espn_stats(year=year, stat_type='passing'),
        'rushing': scraper.get_espn_stats(year=year, stat_type='rushing'),
        'receiving': scraper.get_espn_stats(year=year, stat_type='receiving'),
    }

    return data
