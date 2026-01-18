"""
Data management for the Transfer Portal Dashboard.
Contains mock data for 25 teams and their transfer portal activity.
"""

import pandas as pd
from typing import Dict, List
import random

# Conference mappings
CONFERENCES = {
    "SEC": ["Georgia", "Alabama", "LSU", "Tennessee", "Texas A&M", "Florida", "Auburn", "Ole Miss", "Kentucky", "South Carolina", "Missouri", "Texas", "Oklahoma"],
    "Big Ten": ["Ohio State", "Michigan", "Penn State", "Wisconsin", "Oregon"],
    "Big 12": ["Colorado", "Arizona"],
    "ACC": ["Florida State", "Clemson", "Miami"],
    "Independent": ["Notre Dame"],
    "Pac-12": ["USC"],
}


def get_team_conference(team: str) -> str:
    """Get the conference for a team."""
    for conf, teams in CONFERENCES.items():
        if team in teams:
            return conf
    return "Other"


# Top 25 teams with their transfer portal data
TOP_25_TEAMS = [
    {"rank": 1, "team": "Georgia", "inflows": 14, "outflows": 8, "inflow_value": 12.4, "outflow_value": 4.2, "avg_rating": 94.2},
    {"rank": 2, "team": "Alabama", "inflows": 12, "outflows": 11, "inflow_value": 11.8, "outflow_value": 5.8, "avg_rating": 93.8},
    {"rank": 3, "team": "Ohio State", "inflows": 11, "outflows": 9, "inflow_value": 10.9, "outflow_value": 4.5, "avg_rating": 93.5},
    {"rank": 4, "team": "Texas", "inflows": 13, "outflows": 7, "inflow_value": 10.5, "outflow_value": 3.8, "avg_rating": 93.1},
    {"rank": 5, "team": "Oregon", "inflows": 10, "outflows": 6, "inflow_value": 9.8, "outflow_value": 3.2, "avg_rating": 92.9},
    {"rank": 6, "team": "Penn State", "inflows": 9, "outflows": 8, "inflow_value": 9.2, "outflow_value": 4.1, "avg_rating": 92.4},
    {"rank": 7, "team": "Michigan", "inflows": 8, "outflows": 12, "inflow_value": 8.7, "outflow_value": 6.2, "avg_rating": 92.1},
    {"rank": 8, "team": "Notre Dame", "inflows": 10, "outflows": 5, "inflow_value": 8.5, "outflow_value": 2.9, "avg_rating": 91.8},
    {"rank": 9, "team": "LSU", "inflows": 11, "outflows": 9, "inflow_value": 8.2, "outflow_value": 4.8, "avg_rating": 91.5},
    {"rank": 10, "team": "USC", "inflows": 12, "outflows": 10, "inflow_value": 8.0, "outflow_value": 5.1, "avg_rating": 91.2},
    {"rank": 11, "team": "Florida State", "inflows": 9, "outflows": 11, "inflow_value": 7.8, "outflow_value": 5.5, "avg_rating": 90.8},
    {"rank": 12, "team": "Clemson", "inflows": 8, "outflows": 7, "inflow_value": 7.5, "outflow_value": 3.8, "avg_rating": 90.5},
    {"rank": 13, "team": "Tennessee", "inflows": 10, "outflows": 8, "inflow_value": 7.2, "outflow_value": 4.2, "avg_rating": 90.2},
    {"rank": 14, "team": "Oklahoma", "inflows": 11, "outflows": 13, "inflow_value": 7.0, "outflow_value": 6.5, "avg_rating": 89.8},
    {"rank": 15, "team": "Miami", "inflows": 9, "outflows": 6, "inflow_value": 6.8, "outflow_value": 3.2, "avg_rating": 89.5},
    {"rank": 16, "team": "Florida", "inflows": 8, "outflows": 10, "inflow_value": 6.5, "outflow_value": 5.2, "avg_rating": 89.2},
    {"rank": 17, "team": "Auburn", "inflows": 10, "outflows": 9, "inflow_value": 6.3, "outflow_value": 4.5, "avg_rating": 88.9},
    {"rank": 18, "team": "Texas A&M", "inflows": 9, "outflows": 11, "inflow_value": 6.1, "outflow_value": 5.8, "avg_rating": 88.5},
    {"rank": 19, "team": "Wisconsin", "inflows": 7, "outflows": 8, "inflow_value": 5.9, "outflow_value": 4.2, "avg_rating": 88.2},
    {"rank": 20, "team": "Ole Miss", "inflows": 11, "outflows": 7, "inflow_value": 5.7, "outflow_value": 3.5, "avg_rating": 87.9},
    {"rank": 21, "team": "Colorado", "inflows": 15, "outflows": 14, "inflow_value": 5.5, "outflow_value": 4.8, "avg_rating": 87.5},
    {"rank": 22, "team": "South Carolina", "inflows": 8, "outflows": 9, "inflow_value": 5.2, "outflow_value": 4.5, "avg_rating": 87.2},
    {"rank": 23, "team": "Kentucky", "inflows": 9, "outflows": 8, "inflow_value": 5.0, "outflow_value": 3.8, "avg_rating": 86.8},
    {"rank": 24, "team": "Arizona", "inflows": 10, "outflows": 6, "inflow_value": 4.8, "outflow_value": 2.9, "avg_rating": 86.5},
    {"rank": 25, "team": "Missouri", "inflows": 8, "outflows": 7, "inflow_value": 4.5, "outflow_value": 3.2, "avg_rating": 86.2},
]

# Mock player data for each team
POSITIONS = ["QB", "RB", "WR", "WR", "WR", "TE", "OT", "OG", "C", "OG", "OT", "DE", "DT", "DT", "DE", "LB", "LB", "LB", "CB", "CB", "S", "S"]
FIRST_NAMES = ["Marcus", "Jayden", "Cameron", "Devon", "Tyler", "Brandon", "Justin", "Malik", "Darius", "Antonio", "Chris", "Jordan", "Xavier", "Caleb", "Isaiah", "Tre", "Keon", "Jalen", "Quincy", "Rashad"]
LAST_NAMES = ["Williams", "Johnson", "Smith", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark"]


def generate_player_name():
    """Generate a random player name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_players_for_team(team: str, count: int, is_inflow: bool) -> List[Dict]:
    """Generate mock player data for a team."""
    players = []
    random.seed(hash(team) + (1 if is_inflow else 0))  # Consistent random for same team

    for i in range(count):
        # Generate high school rating (0.8000 - 1.0000 scale)
        hs_rating = round(random.uniform(0.8200, 0.9900), 4)

        # Some players have game experience, some don't
        has_game_experience = random.random() > 0.3
        games_played = random.randint(1, 40) if has_game_experience else 0

        # Calculate player value based on our methodology
        from src.valuation import calculate_player_value
        value_data = calculate_player_value(
            hs_rating=hs_rating,
            games_played=games_played,
            stats_percentile=random.uniform(0.3, 0.95) if has_game_experience else 0,
            position=random.choice(POSITIONS)
        )

        player = {
            "name": generate_player_name(),
            "position": random.choice(POSITIONS),
            "hs_rating": hs_rating,
            "hs_rank": random.randint(1, 500),
            "games_played": games_played,
            "stats_percentile": round(random.uniform(0.3, 0.95), 2) if has_game_experience else None,
            "value": value_data["value"],
            "value_breakdown": value_data["breakdown"],
            "previous_team" if is_inflow else "new_team": random.choice([t["team"] for t in TOP_25_TEAMS if t["team"] != team]),
            "status": random.choice(["Committed", "Enrolled"]) if is_inflow else "Entered Portal",
            "transfer_date": f"Jan {random.randint(1, 17)}, 2026"
        }
        players.append(player)

    return players


def get_team_data() -> pd.DataFrame:
    """Get the top 25 teams data as a DataFrame."""
    df = pd.DataFrame(TOP_25_TEAMS)
    df["conference"] = df["team"].apply(get_team_conference)
    df["net_value"] = df["inflow_value"] - df["outflow_value"]
    return df


def get_team_details(team_name: str) -> Dict:
    """Get detailed data for a specific team."""
    team_data = next((t for t in TOP_25_TEAMS if t["team"] == team_name), None)
    if not team_data:
        return None

    return {
        "info": team_data,
        "conference": get_team_conference(team_name),
        "inflows": generate_players_for_team(team_name, team_data["inflows"], is_inflow=True),
        "outflows": generate_players_for_team(team_name, team_data["outflows"], is_inflow=False),
    }


def get_all_teams_list() -> List[str]:
    """Get list of all team names."""
    return [t["team"] for t in TOP_25_TEAMS]


def get_summary_stats() -> Dict:
    """Get summary statistics for the dashboard."""
    df = get_team_data()
    return {
        "total_transfers": int(df["inflows"].sum() + df["outflows"].sum()),
        "total_inflows": int(df["inflows"].sum()),
        "total_outflows": int(df["outflows"].sum()),
        "total_value": round(df["inflow_value"].sum(), 1),
        "avg_rating": round(df["avg_rating"].mean(), 1),
        "teams_tracked": len(TOP_25_TEAMS),
    }
