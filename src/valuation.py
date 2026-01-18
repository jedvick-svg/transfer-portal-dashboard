"""
Player Valuation Methodology

This module implements the player value calculation based on:
1. High school recruiting rankings (247Sports composite)
2. Actual game performance stats from ESPN
3. Position-specific adjustments

The weighting between HS data and game stats depends on experience:
- Players with 0-5 games: 90% HS rating, 10% stats (if any)
- Players with 6-20 games: 50% HS rating, 50% stats
- Players with 21+ games: 20% HS rating, 80% stats
"""

from typing import Dict, Optional

# Position value multipliers (QBs and edge rushers command premium)
POSITION_MULTIPLIERS = {
    "QB": 1.50,    # Quarterbacks are most valuable
    "DE": 1.20,   # Edge rushers
    "OT": 1.15,   # Left tackle especially valuable
    "CB": 1.10,   # Cornerbacks
    "WR": 1.05,   # Wide receivers
    "LB": 1.00,   # Linebackers (baseline)
    "DT": 1.00,   # Defensive tackles
    "S": 0.95,    # Safeties
    "RB": 0.90,   # Running backs (shorter careers)
    "TE": 0.90,   # Tight ends
    "OG": 0.85,   # Guards
    "C": 0.80,    # Centers
    "K/P": 0.50,  # Specialists
}

# Base value ranges in millions
BASE_VALUE_MIN = 0.1  # $100K minimum
BASE_VALUE_MAX = 3.5  # $3.5M maximum for top players


def get_hs_weight(games_played: int) -> float:
    """
    Determine how much weight to give high school ranking vs game stats.

    Returns the weight for HS rating (1 - this = stats weight)
    """
    if games_played <= 5:
        return 0.90  # Heavily weighted toward HS for freshmen/limited experience
    elif games_played <= 20:
        return 0.50  # Balanced for players with moderate experience
    else:
        return 0.20  # Experienced players judged mostly on performance


def normalize_hs_rating(rating: float) -> float:
    """
    Normalize 247Sports composite rating to 0-1 scale.

    247 ratings typically range from 0.7000 (2-star) to 1.0000 (5-star)
    We normalize so that:
    - 0.7000 -> 0.0
    - 1.0000 -> 1.0
    """
    return max(0, min(1, (rating - 0.7000) / 0.3000))


def calculate_raw_value(normalized_score: float) -> float:
    """
    Convert normalized score (0-1) to dollar value.

    Uses exponential scaling so top players are worth significantly more.
    """
    # Exponential curve: value = min + (max - min) * score^1.5
    return BASE_VALUE_MIN + (BASE_VALUE_MAX - BASE_VALUE_MIN) * (normalized_score ** 1.5)


def calculate_player_value(
    hs_rating: float,
    games_played: int = 0,
    stats_percentile: Optional[float] = None,
    position: str = "LB"
) -> Dict:
    """
    Calculate a player's transfer portal value.

    Args:
        hs_rating: 247Sports composite rating (0.7000 - 1.0000)
        games_played: Number of college games played
        stats_percentile: Performance percentile (0-1) if available
        position: Player position code

    Returns:
        Dict with 'value' (in millions) and 'breakdown' explaining calculation
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
        composite_score = hs_normalized  # No stats available, use HS only

    # Get position multiplier
    pos_mult = POSITION_MULTIPLIERS.get(position, 1.0)

    # Calculate raw value
    raw_value = calculate_raw_value(composite_score)

    # Apply position multiplier
    final_value = raw_value * pos_mult

    # Build breakdown
    breakdown = {
        "hs_rating": hs_rating,
        "hs_normalized": round(hs_normalized, 3),
        "hs_weight": hs_weight,
        "stats_percentile": stats_percentile,
        "stats_weight": stats_weight,
        "composite_score": round(composite_score, 3),
        "position_multiplier": pos_mult,
        "raw_value": round(raw_value, 3),
        "final_value": round(final_value, 3),
    }

    return {
        "value": round(final_value, 2),
        "breakdown": breakdown,
    }


def get_methodology_text() -> Dict[str, str]:
    """
    Get the methodology explanation text for the website.
    """
    return {
        "overview": """
Our player valuation model combines high school recruiting data with actual
game performance to estimate a player's transfer portal value. The model
adapts its weighting based on how much college experience a player has.
        """,

        "data_sources": """
**High School Data (247Sports Composite)**
- 247Sports composite ratings aggregate rankings from major recruiting services
- Ratings range from 0.7000 (2-star) to 1.0000 (5-star recruit)
- We normalize these to a 0-1 scale for calculations

**Game Performance Data (ESPN)**
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

        "position_adjustments": """
Not all positions are valued equally in the transfer market. Quarterbacks
and premium pass rushers command the highest values:

| Position | Multiplier | Rationale |
|----------|------------|-----------|
| QB       | 1.50x      | Most impactful position |
| DE       | 1.20x      | Premium pass rushers |
| OT       | 1.15x      | Protect the QB |
| CB       | 1.10x      | Cover the pass |
| WR       | 1.05x      | Playmakers |
| LB/DT    | 1.00x      | Baseline |
| S/RB/TE  | 0.90-0.95x | Important but replaceable |
| OG/C     | 0.80-0.85x | Interior line depth |
| K/P      | 0.50x      | Specialists |
        """,

        "formula": """
```
Player Value = Base Value × Position Multiplier

Where:
  Base Value = $0.1M + ($3.5M - $0.1M) × Composite Score^1.5

  Composite Score = (HS_Normalized × HS_Weight) + (Stats_Percentile × Stats_Weight)

  HS_Normalized = (HS_Rating - 0.7000) / 0.3000
```

The exponential factor (^1.5) ensures elite players are valued
disproportionately higher than average players.
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
