"""
Data management for NIL or Nothing Transfer Portal Dashboard.
Contains sample data for 25 teams and their transfer portal activity.

NOTE: This dashboard uses SAMPLE DATA for demonstration purposes.
Real-time transfer portal data would require integration with 247Sports,
On3, Rivals, or ESPN APIs which require authentication and licensing.
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

# Player classes for weighting
PLAYER_CLASSES = [
    "Freshman", "Redshirt Freshman", "Sophomore", "Redshirt Sophomore",
    "Junior", "Redshirt Junior", "Senior", "Redshirt Senior", "Graduate"
]

# Class probabilities (transfers tend to be upperclassmen)
CLASS_PROBABILITIES = {
    "Freshman": 0.02,
    "Redshirt Freshman": 0.05,
    "Sophomore": 0.10,
    "Redshirt Sophomore": 0.12,
    "Junior": 0.18,
    "Redshirt Junior": 0.15,
    "Senior": 0.15,
    "Redshirt Senior": 0.13,
    "Graduate": 0.10,
}


def get_team_conference(team: str) -> str:
    """Get the conference for a team."""
    for conf, teams in CONFERENCES.items():
        if team in teams:
            return conf
    return "Other"


def get_random_class() -> str:
    """Get a weighted random player class."""
    classes = list(CLASS_PROBABILITIES.keys())
    weights = list(CLASS_PROBABILITIES.values())
    return random.choices(classes, weights=weights, k=1)[0]


# Positions with offensive/defensive categorization
OFFENSIVE_POSITIONS = ["QB", "RB", "WR", "TE", "OT", "OG", "C"]
DEFENSIVE_POSITIONS = ["DE", "DT", "LB", "CB", "S", "EDGE"]
ALL_POSITIONS = OFFENSIVE_POSITIONS + DEFENSIVE_POSITIONS

# Sample player names
FIRST_NAMES = ["Marcus", "Jayden", "Cameron", "Devon", "Tyler", "Brandon", "Justin", "Malik", "Darius", "Antonio",
               "Chris", "Jordan", "Xavier", "Caleb", "Isaiah", "Tre", "Keon", "Jalen", "Quincy", "Rashad",
               "Bryce", "Trey", "DeVonte", "Marvin", "Keontae", "Jaylon", "Deon", "Terrell", "Kyler", "Jameson"]
LAST_NAMES = ["Williams", "Johnson", "Smith", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson",
              "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark",
              "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright", "Scott", "Green"]


def generate_player_name():
    """Generate a random player name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_players_for_team(team: str, count: int, is_inflow: bool) -> List[Dict]:
    """Generate sample player data for a team with scoring."""
    players = []
    random.seed(hash(team) + (1 if is_inflow else 0))

    for i in range(count):
        # Generate high school rating (0.8000 - 1.0000 scale)
        hs_rating = round(random.uniform(0.8200, 0.9900), 4)

        # Some players have game experience
        has_game_experience = random.random() > 0.3
        games_played = random.randint(1, 40) if has_game_experience else 0

        # Assign position
        position = random.choice(ALL_POSITIONS)

        # Assign class
        player_class = get_random_class()

        # Calculate player value and score
        from src.valuation import calculate_player_value
        value_data = calculate_player_value(
            hs_rating=hs_rating,
            games_played=games_played,
            stats_percentile=random.uniform(0.3, 0.95) if has_game_experience else 0,
            position=position,
            player_class=player_class
        )

        player = {
            "name": generate_player_name(),
            "position": position,
            "player_class": player_class,
            "hs_rating": hs_rating,
            "hs_rank": random.randint(1, 500),
            "games_played": games_played,
            "stats_percentile": round(random.uniform(0.3, 0.95), 2) if has_game_experience else None,
            "value": value_data["value"],
            "score": value_data["score"],
            "value_breakdown": value_data["breakdown"],
            "previous_team" if is_inflow else "new_team": random.choice([t["team"] for t in TOP_25_TEAMS if t["team"] != team]),
            "status": random.choice(["Committed", "Enrolled"]) if is_inflow else "Entered Portal",
            "transfer_date": f"Jan {random.randint(1, 17)}, 2026"
        }
        players.append(player)

    return players


def calculate_team_data_with_scores() -> List[Dict]:
    """Calculate team data with proper scoring system."""
    teams_with_scores = []

    for team_base in TOP_25_TEAMS:
        team_name = team_base["team"]

        # Generate player data
        inflows = generate_players_for_team(team_name, team_base["inflows"], is_inflow=True)
        outflows = generate_players_for_team(team_name, team_base["outflows"], is_inflow=False)

        # Calculate scores
        from src.valuation import calculate_team_score
        score_data = calculate_team_score(inflows, outflows)

        # Calculate NIL spent (sum of incoming player values)
        nil_spent = sum(p["value"] for p in inflows)

        team_data = {
            "team": team_name,
            "score": score_data["total_score"],
            "incoming_score": score_data["incoming_score"],
            "outgoing_score": score_data["outgoing_score"],
            "nil_spent": round(nil_spent, 2),
            "inflows": team_base["inflows"],
            "outflows": team_base["outflows"],
            "offensive_in": score_data["offensive_in"],
            "offensive_out": score_data["offensive_out"],
            "offensive_net": score_data["offensive_net"],
            "defensive_in": score_data["defensive_in"],
            "defensive_out": score_data["defensive_out"],
            "defensive_net": score_data["defensive_net"],
            "conference": get_team_conference(team_name),
            "avg_rating": team_base["avg_rating"],
        }
        teams_with_scores.append(team_data)

    # Sort by score descending and assign ranks
    teams_with_scores.sort(key=lambda x: x["score"], reverse=True)
    for i, team in enumerate(teams_with_scores):
        team["rank"] = i + 1

    return teams_with_scores


# Base team data (will be enhanced with scoring)
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


def get_team_data() -> pd.DataFrame:
    """Get the team data as a DataFrame, sorted by score."""
    teams_with_scores = calculate_team_data_with_scores()
    df = pd.DataFrame(teams_with_scores)
    return df


def get_team_details(team_name: str) -> Dict:
    """Get detailed data for a specific team."""
    team_base = next((t for t in TOP_25_TEAMS if t["team"] == team_name), None)
    if not team_base:
        return None

    # Generate player data with scores
    inflows = generate_players_for_team(team_name, team_base["inflows"], is_inflow=True)
    outflows = generate_players_for_team(team_name, team_base["outflows"], is_inflow=False)

    # Calculate team scores
    from src.valuation import calculate_team_score
    score_data = calculate_team_score(inflows, outflows)

    # Get the rank from scored data
    all_teams = calculate_team_data_with_scores()
    team_rank_data = next((t for t in all_teams if t["team"] == team_name), None)

    return {
        "info": {
            **team_base,
            "rank": team_rank_data["rank"] if team_rank_data else team_base["rank"],
            "score": score_data["total_score"],
            "nil_spent": round(sum(p["value"] for p in inflows), 2),
            "offensive_net": score_data["offensive_net"],
            "defensive_net": score_data["defensive_net"],
        },
        "conference": get_team_conference(team_name),
        "inflows": inflows,
        "outflows": outflows,
        "score_data": score_data,
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
        "total_nil_spent": round(df["nil_spent"].sum(), 1),
        "avg_score": round(df["score"].mean(), 1),
        "teams_tracked": len(TOP_25_TEAMS),
    }


def get_all_transfers() -> pd.DataFrame:
    """Get all transfer data from all teams for the database."""
    all_transfers = []
    teams = get_all_teams_list()

    for team in teams:
        team_data = get_team_details(team)
        if team_data:
            # Add inflows
            for player in team_data["inflows"]:
                all_transfers.append({
                    "Player": player["name"],
                    "Position": player["position"],
                    "Class": player["player_class"],
                    "From": player.get("previous_team", "Unknown"),
                    "To": team,
                    "Rating": player["hs_rating"],
                    "Score": player["score"],
                    "Value ($M)": player["value"],
                    "Games": player["games_played"],
                    "Date Transferred": player.get("transfer_date", "Jan 2026"),
                    "Type": "Inflow",
                    "Conference": team_data["conference"]
                })

            # Add outflows
            for player in team_data["outflows"]:
                all_transfers.append({
                    "Player": player["name"],
                    "Position": player["position"],
                    "Class": player["player_class"],
                    "From": team,
                    "To": player.get("new_team", "TBD"),
                    "Rating": player["hs_rating"],
                    "Score": player["score"],
                    "Value ($M)": player["value"],
                    "Games": player["games_played"],
                    "Date Transferred": player.get("transfer_date", "Jan 2026"),
                    "Type": "Outflow",
                    "Conference": team_data["conference"]
                })

    return pd.DataFrame(all_transfers)
