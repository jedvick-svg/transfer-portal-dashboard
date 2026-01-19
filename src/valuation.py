"""
Player Valuation Methodology for NIL or Nothing

This module implements the player scoring and value calculation based on:
1. High school recruiting rankings (247Sports composite)
2. Actual game performance stats
3. Position-specific multipliers
4. Class/eligibility weights

Scoring Formula:
Score = Σ(Player Rating × Position Multiplier × Class Weight) for gains
      - Σ(Player Rating × Position Multiplier × Class Weight) for losses
"""

from typing import Dict, Optional, List

# Class weights - more experienced players have immediate impact
CLASS_WEIGHTS = {
    "Freshman": 0.70,
    "Redshirt Freshman": 0.75,
    "Sophomore": 0.85,
    "Redshirt Sophomore": 0.90,
    "Junior": 0.95,
    "Redshirt Junior": 1.00,
    "Senior": 1.05,
    "Redshirt Senior": 1.10,
    "Graduate": 1.15,
}

# Position value multipliers with detailed reasoning
POSITION_MULTIPLIERS = {
    "QB": 1.50,
    "DE": 1.25,
    "EDGE": 1.25,
    "OT": 1.20,
    "CB": 1.15,
    "WR": 1.10,
    "DT": 1.05,
    "LB": 1.00,
    "S": 0.95,
    "TE": 0.90,
    "RB": 0.85,
    "OG": 0.85,
    "C": 0.80,
    "K": 0.50,
    "P": 0.50,
    "K/P": 0.50,
    "LS": 0.45,
}

# Detailed position multiplier explanations
POSITION_MULTIPLIER_REASONING = {
    "QB": {
        "multiplier": 1.50,
        "reasoning": "Quarterbacks receive the highest multiplier due to their outsized impact on team success. They touch the ball on every offensive play, make pre-snap reads, and are responsible for executing the entire offensive scheme. Historically, transfer QBs like Joe Burrow (LSU), Jalen Hurts (Oklahoma), and Caleb Williams (USC) have led teams to championships. Elite QB talent is scarce, and a single high-quality transfer can transform a program's trajectory overnight."
    },
    "DE": {
        "multiplier": 1.25,
        "reasoning": "Edge rushers and defensive ends are premium defensive assets because they directly disrupt opposing offenses at the point of attack. Their ability to generate sacks and pressure quarterbacks can single-handedly change games. Transfer edge rushers like Will Anderson Jr. and Dallas Turner have made immediate impacts. The position requires rare athleticism—speed, power, and technique—making elite talent difficult to develop and highly valuable in the portal."
    },
    "EDGE": {
        "multiplier": 1.25,
        "reasoning": "Modern edge defenders (OLB/DE hybrids) are crucial in today's spread-heavy offenses. They must defend the run, rush the passer, and occasionally drop into coverage. This versatility commands a premium as defenses need players who can handle multiple responsibilities without substitution."
    },
    "OT": {
        "multiplier": 1.20,
        "reasoning": "Offensive tackles, particularly left tackles, protect the quarterback's blind side and are essential for both passing and running games. Quality tackle play takes years to develop, and experienced transfers at this position provide immediate stability. Programs consistently invest heavily in portal OTs because poor tackle play leads to sacks, turnovers, and quarterback injuries."
    },
    "CB": {
        "multiplier": 1.15,
        "reasoning": "Cornerbacks operate in isolation against opposing receivers and must make split-second decisions with minimal help. One weak corner can be exploited repeatedly by opponents. Transfer corners with proven ball skills and experience against high-level competition are highly valued because developing elite coverage ability typically requires years of seasoning."
    },
    "WR": {
        "multiplier": 1.10,
        "reasoning": "Wide receivers create explosive plays and serve as primary targets in modern spread offenses. Quality depth at receiver is essential for sustaining drives and scoring touchdowns. Transfer receivers who have proven they can separate and catch in traffic provide immediate offensive weapons, though the position's depth across college football slightly moderates the premium."
    },
    "DT": {
        "multiplier": 1.05,
        "reasoning": "Defensive tackles anchor the defense by controlling the line of scrimmage and collapsing the pocket. They require significant size and strength that takes time to develop. Transfer DTs who can occupy multiple blockers free up linebackers and edge rushers. The position is slightly less premium than edge rusher due to typically lower individual statistics."
    },
    "LB": {
        "multiplier": 1.00,
        "reasoning": "Linebackers serve as the defensive baseline—important players who make tackles, defend the run, and contribute in coverage. They represent the standard against which other positions are measured. Good linebacker play is essential but doesn't carry the same premium as positions that directly create turnovers or touchdowns."
    },
    "S": {
        "multiplier": 0.95,
        "reasoning": "Safeties provide the last line of defense and are critical for preventing big plays. However, they typically operate in a support role rather than making game-changing individual plays. Slot coverage duties in modern football have increased their importance, but overall depth at the position keeps premiums modest."
    },
    "TE": {
        "multiplier": 0.90,
        "reasoning": "Tight ends are versatile players who block and receive, but few programs feature them prominently in their offenses. Elite receiving tight ends are valuable, but many teams can succeed without a star at the position. The dual-role nature means players must master two skill sets, which limits the available elite talent pool."
    },
    "RB": {
        "multiplier": 0.85,
        "reasoning": "Running backs, while exciting playmakers, have shorter prime windows and are generally considered more replaceable than other skill positions. The rise of running back committees and the physical toll of the position means teams often prefer spreading carries among multiple backs rather than investing heavily in a single transfer."
    },
    "OG": {
        "multiplier": 0.85,
        "reasoning": "Interior offensive linemen (guards) are important for run blocking and interior pass protection but are less visible than tackles. Quality guard play matters, but the position receives less premium because guards face fewer athletic edge rushers and have more help from adjacent linemen."
    },
    "C": {
        "multiplier": 0.80,
        "reasoning": "Centers anchor the offensive line and make protection calls, requiring high football IQ. However, the position is often overlooked in recruiting and the transfer market because athletic demands are lower than other line positions. Experienced centers provide stability but rarely command significant NIL investment."
    },
    "K": {
        "multiplier": 0.50,
        "reasoning": "Kickers handle field goals and kickoffs—important but limited roles. They play on a small fraction of total snaps, and while clutch kicking matters, the position doesn't warrant significant investment compared to full-time players who impact every drive."
    },
    "P": {
        "multiplier": 0.50,
        "reasoning": "Punters flip field position and can be valuable in close games, but like kickers, their limited role means lower investment priority. Good punting is appreciated but rarely determines games at the same level as other positions."
    },
    "LS": {
        "multiplier": 0.45,
        "reasoning": "Long snappers are specialists noticed only when they make mistakes. While consistency is important for field goals and punts, the position requires the least athletic ability and has the smallest impact on game outcomes of any scholarship position."
    },
}

# Base value ranges in millions
BASE_VALUE_MIN = 0.1  # $100K minimum
BASE_VALUE_MAX = 3.5  # $3.5M maximum for top players


def get_class_weight(player_class: str) -> float:
    """Get the weight multiplier for a player's class."""
    return CLASS_WEIGHTS.get(player_class, 1.0)


def get_hs_weight(games_played: int) -> float:
    """
    Determine how much weight to give high school ranking vs game stats.
    Returns the weight for HS rating (1 - this = stats weight)
    """
    if games_played <= 5:
        return 0.90
    elif games_played <= 20:
        return 0.50
    else:
        return 0.20


def normalize_hs_rating(rating: float) -> float:
    """
    Normalize 247Sports composite rating to 0-1 scale.
    247 ratings typically range from 0.7000 (2-star) to 1.0000 (5-star)
    """
    return max(0, min(1, (rating - 0.7000) / 0.3000))


def calculate_raw_value(normalized_score: float) -> float:
    """Convert normalized score (0-1) to dollar value using exponential scaling."""
    return BASE_VALUE_MIN + (BASE_VALUE_MAX - BASE_VALUE_MIN) * (normalized_score ** 1.5)


def calculate_player_score(
    hs_rating: float,
    games_played: int = 0,
    stats_percentile: Optional[float] = None,
    position: str = "LB",
    player_class: str = "Junior"
) -> Dict:
    """
    Calculate a player's transfer portal SCORE (not dollar value).

    Score = Normalized Rating × Position Multiplier × Class Weight
    """
    # Normalize HS rating
    hs_normalized = normalize_hs_rating(hs_rating)

    # Get weighting
    hs_weight = get_hs_weight(games_played)
    stats_weight = 1 - hs_weight

    # Calculate composite score
    if stats_percentile is not None and games_played > 0:
        composite_score = (hs_normalized * hs_weight) + (stats_percentile * stats_weight)
    else:
        composite_score = hs_normalized

    # Get multipliers
    pos_mult = POSITION_MULTIPLIERS.get(position, 1.0)
    class_mult = get_class_weight(player_class)

    # Calculate final score (0-100 scale)
    raw_score = composite_score * 100
    final_score = raw_score * pos_mult * class_mult

    return {
        "score": round(final_score, 2),
        "raw_score": round(raw_score, 2),
        "position_multiplier": pos_mult,
        "class_multiplier": class_mult,
        "composite_score": round(composite_score, 3),
    }


def calculate_player_value(
    hs_rating: float,
    games_played: int = 0,
    stats_percentile: Optional[float] = None,
    position: str = "LB",
    player_class: str = "Junior"
) -> Dict:
    """
    Calculate a player's transfer portal value (NIL estimate in millions).
    """
    # Normalize HS rating
    hs_normalized = normalize_hs_rating(hs_rating)

    # Get weighting
    hs_weight = get_hs_weight(games_played)
    stats_weight = 1 - hs_weight

    # Calculate composite score
    if stats_percentile is not None and games_played > 0:
        composite_score = (hs_normalized * hs_weight) + (stats_percentile * stats_weight)
    else:
        composite_score = hs_normalized

    # Get position multiplier
    pos_mult = POSITION_MULTIPLIERS.get(position, 1.0)
    class_mult = get_class_weight(player_class)

    # Calculate raw value
    raw_value = calculate_raw_value(composite_score)

    # Apply multipliers
    final_value = raw_value * pos_mult * class_mult

    # Calculate score as well
    score_data = calculate_player_score(hs_rating, games_played, stats_percentile, position, player_class)

    # Build breakdown
    breakdown = {
        "hs_rating": hs_rating,
        "hs_normalized": round(hs_normalized, 3),
        "hs_weight": hs_weight,
        "stats_percentile": stats_percentile,
        "stats_weight": stats_weight,
        "composite_score": round(composite_score, 3),
        "position_multiplier": pos_mult,
        "class_weight": class_mult,
        "raw_value": round(raw_value, 3),
        "final_value": round(final_value, 3),
        "player_score": score_data["score"],
    }

    return {
        "value": round(final_value, 2),
        "score": score_data["score"],
        "breakdown": breakdown,
    }


def calculate_team_score(inflows: List[Dict], outflows: List[Dict]) -> Dict:
    """
    Calculate a team's total transfer portal score.

    Score = Σ(incoming player scores) - Σ(outgoing player scores)
    """
    incoming_score = sum(p.get("score", 0) for p in inflows)
    outgoing_score = sum(p.get("score", 0) for p in outflows)

    # Count offensive vs defensive players
    offensive_positions = {"QB", "RB", "WR", "TE", "OT", "OG", "C"}
    defensive_positions = {"DE", "EDGE", "DT", "LB", "CB", "S"}

    off_in = sum(1 for p in inflows if p.get("position") in offensive_positions)
    off_out = sum(1 for p in outflows if p.get("position") in offensive_positions)
    def_in = sum(1 for p in inflows if p.get("position") in defensive_positions)
    def_out = sum(1 for p in outflows if p.get("position") in defensive_positions)

    return {
        "total_score": round(incoming_score - outgoing_score, 2),
        "incoming_score": round(incoming_score, 2),
        "outgoing_score": round(outgoing_score, 2),
        "offensive_net": off_in - off_out,
        "offensive_in": off_in,
        "offensive_out": off_out,
        "defensive_net": def_in - def_out,
        "defensive_in": def_in,
        "defensive_out": def_out,
    }


def get_position_multipliers_table() -> List[Dict]:
    """Get position multipliers with full reasoning for display."""
    table_data = []
    for pos in ["QB", "DE", "EDGE", "OT", "CB", "WR", "DT", "LB", "S", "TE", "RB", "OG", "C", "K", "P", "LS"]:
        if pos in POSITION_MULTIPLIER_REASONING:
            data = POSITION_MULTIPLIER_REASONING[pos]
            table_data.append({
                "position": pos,
                "multiplier": data["multiplier"],
                "reasoning": data["reasoning"]
            })
    return table_data


def get_methodology_text() -> Dict[str, str]:
    """Get the methodology explanation text for the website."""
    return {
        "overview": """
NIL or Nothing uses a proprietary scoring system to evaluate transfer portal activity.
Our model combines recruiting rankings, on-field performance, positional value, and
player experience to create a comprehensive score for each transfer. Teams are then
ranked by their net score: the sum of incoming player scores minus outgoing player scores.
        """,

        "data_sources": """
**High School Data (247Sports Composite)**
- 247Sports composite ratings aggregate rankings from major recruiting services
- Ratings range from 0.7000 (2-star) to 1.0000 (5-star recruit)
- We normalize these to a 0-1 scale for calculations

**Game Performance Data**
- Passing, rushing, receiving yards and touchdowns
- Defensive stats: tackles, sacks, interceptions
- Converted to a percentile ranking among all FBS players at the position
        """,

        "weighting": """
The balance between high school rating and game stats depends on experience:

| Games Played | HS Weight | Stats Weight |
|-------------|-----------|--------------|
| 0-5 games   | 90%       | 10%          |
| 6-20 games  | 50%       | 50%          |
| 21+ games   | 20%       | 80%          |

This approach recognizes that recruits with limited college tape should be
evaluated primarily on their recruiting profile, while experienced players
are judged more on actual performance.
        """,

        "class_weights": """
Player class affects their immediate impact potential:

| Class | Weight | Rationale |
|-------|--------|-----------|
| Graduate | 1.15x | Immediate eligibility, experienced leadership |
| Redshirt Senior | 1.10x | Seasoned player, one year remaining |
| Senior | 1.05x | Experienced, immediate contributor |
| Redshirt Junior | 1.00x | Baseline - full experience |
| Junior | 0.95x | Good experience level |
| Redshirt Sophomore | 0.90x | Developing, some experience |
| Sophomore | 0.85x | Limited experience |
| Redshirt Freshman | 0.75x | Minimal college experience |
| Freshman | 0.70x | No college experience |
        """,

        "limitations": """
**Important Caveats:**

1. **NIL Market Dynamics**: Actual NIL deals depend on marketability,
   social following, and team needs—factors we don't model.

2. **Scheme Fit**: A player's value varies significantly based on how
   well they fit a team's scheme.

3. **Character/Leadership**: Intangibles matter but aren't quantifiable.

4. **Injury History**: Not currently factored into valuations.

5. **Market Timing**: Portal values fluctuate based on supply/demand.

This model provides a baseline estimate, not a guaranteed market value.
        """
    }
