"""
News Feed for Transfer Portal Updates - NIL or Nothing

Fetches and displays latest transfer portal news from various sources.
In production, this would use APIs or RSS feeds. For now, using sample data.

NOTE: This uses SAMPLE DATA for demonstration purposes.
Real-time news would require integration with sports news APIs.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict

# Sample news data - in production, this would be scraped/fetched from APIs
MOCK_NEWS = [
    # Commitments
    {
        "source": "ESPN",
        "title": "Five-star QB Jayden Michaels commits to Georgia from Oregon transfer portal",
        "summary": "The highly-touted quarterback announced his decision via social media, citing the Bulldogs' pro-style offense and NIL opportunities.",
        "url": "https://espn.com",
        "category": "commitment"
    },
    {
        "source": "247Sports",
        "title": "BREAKING: Alabama lands top-rated portal WR from USC",
        "summary": "The Crimson Tide continues to reload at receiver with another high-profile addition worth an estimated $1.2M NIL deal.",
        "url": "https://247sports.com",
        "category": "commitment"
    },
    {
        "source": "247Sports",
        "title": "Colorado adds fourth portal commit as Deion Sanders reloads roster",
        "summary": "The Buffaloes continue aggressive portal strategy entering Year 3 of the Coach Prime era.",
        "url": "https://247sports.com",
        "category": "commitment"
    },
    {
        "source": "Rivals",
        "title": "Oklahoma rebuilding secondary through portal acquisitions",
        "summary": "Sooners have added three DBs in the last week to address key need ahead of SEC play.",
        "url": "https://rivals.com",
        "category": "commitment"
    },
    {
        "source": "On3",
        "title": "Texas lands former All-SEC offensive tackle from Florida",
        "summary": "The Longhorns add a key piece to their offensive line with a proven SEC starter.",
        "url": "https://on3.com",
        "category": "commitment"
    },
    # Portal Entries
    {
        "source": "On3",
        "title": "Ohio State starting linebacker enters transfer portal",
        "summary": "The two-year starter announced his decision following the coaching staff changes this offseason.",
        "url": "https://on3.com",
        "category": "entry"
    },
    {
        "source": "ESPN",
        "title": "Michigan loses third defensive starter to portal this week",
        "summary": "The exodus continues in Ann Arbor as another key contributor seeks a new opportunity.",
        "url": "https://espn.com",
        "category": "entry"
    },
    {
        "source": "On3",
        "title": "BREAKING: Former five-star RB enters portal after position change request",
        "summary": "The talented back was asked to move to receiver and declined, now seeking a fresh start.",
        "url": "https://on3.com",
        "category": "entry"
    },
    {
        "source": "247Sports",
        "title": "Auburn QB enters portal after losing starting job competition",
        "summary": "The redshirt junior will seek a starting opportunity elsewhere after two seasons as a backup.",
        "url": "https://247sports.com",
        "category": "entry"
    },
    # Official Visits
    {
        "source": "247Sports",
        "title": "Top portal CB schedules official visit to USC this weekend",
        "summary": "The former SEC starter is down to USC, Oregon, and Miami as he makes his final decision.",
        "url": "https://247sports.com",
        "category": "visit"
    },
    {
        "source": "On3",
        "title": "Five-star portal WR completes Texas A&M official visit",
        "summary": "The Aggies made a strong impression with NIL presentation and facility tour.",
        "url": "https://on3.com",
        "category": "visit"
    },
    {
        "source": "Rivals",
        "title": "Penn State hosting three top portal targets this weekend",
        "summary": "The Nittany Lions looking to close strong on key defensive additions.",
        "url": "https://rivals.com",
        "category": "visit"
    },
    # De-commitments
    {
        "source": "ESPN",
        "title": "BREAKING: Portal commit flips from Ole Miss to Alabama",
        "summary": "The four-star defensive tackle changed his decision after a late visit to Tuscaloosa.",
        "url": "https://espn.com",
        "category": "decommit"
    },
    {
        "source": "On3",
        "title": "Tennessee portal commit backs off pledge, reopens recruitment",
        "summary": "The former Pac-12 starter cited 'personal reasons' for reopening his recruitment.",
        "url": "https://on3.com",
        "category": "decommit"
    },
    # Rumors
    {
        "source": "Twitter / X",
        "title": "Pete Thamel: Texas expected to land commitment from portal OT this week",
        "summary": "Sources indicate the Longhorns are the frontrunner for the former SEC starter.",
        "url": "https://twitter.com",
        "category": "rumor"
    },
    {
        "source": "Twitter / X",
        "title": "Bruce Feldman: Penn State in final three for top portal DT",
        "summary": "The Nittany Lions pushing hard to add interior defensive line depth for 2026.",
        "url": "https://twitter.com",
        "category": "rumor"
    },
    {
        "source": "Twitter / X",
        "title": "Matt Zenitz: Florida State portal target down to FSU and Miami",
        "summary": "In-state battle brewing for talented defensive back with a decision expected soon.",
        "url": "https://twitter.com",
        "category": "rumor"
    },
    {
        "source": "Rivals",
        "title": "EXCLUSIVE: Inside LSU's portal pitch to top remaining recruits",
        "summary": "Tigers selling NIL opportunities and immediate playing time to priority targets.",
        "url": "https://rivals.com",
        "category": "rumor"
    },
    # Analysis
    {
        "source": "Rivals",
        "title": "Transfer Portal Rankings Update: Top 50 players still available",
        "summary": "Our updated rankings of the best players still looking for a new home in 2026.",
        "url": "https://rivals.com",
        "category": "analysis"
    },
    {
        "source": "On3",
        "title": "NIL Analysis: What top portal targets are commanding in the market",
        "summary": "Breaking down the financial landscape of this year's most sought-after transfers.",
        "url": "https://on3.com",
        "category": "analysis"
    },
    {
        "source": "ESPN",
        "title": "Notre Dame quietly building elite portal class under radar",
        "summary": "The Irish have secured commitments from three four-star portal entries with minimal fanfare.",
        "url": "https://espn.com",
        "category": "analysis"
    },
    {
        "source": "247Sports",
        "title": "SEC leads all conferences in portal acquisitions by value",
        "summary": "Analysis shows SEC teams have committed more NIL to portal players than any other league.",
        "url": "https://247sports.com",
        "category": "analysis"
    },
    {
        "source": "On3",
        "title": "Portal Class Rankings: Who's winning the 2026 transfer window?",
        "summary": "Georgia, Alabama, and Texas lead our composite rankings of portal success this cycle.",
        "url": "https://on3.com",
        "category": "analysis"
    },
]

# Source colors for styling
SOURCE_COLORS = {
    "ESPN": "#d00",
    "247Sports": "#0066cc",
    "On3": "#00a651",
    "Twitter / X": "#1da1f2",
    "Rivals": "#ff6b00",
}

# Category icons
CATEGORY_ICONS = {
    "commitment": "checkmark-circle",
    "entry": "arrow-right-circle",
    "rumor": "information-circle",
    "analysis": "bar-chart",
}


def get_time_ago(minutes: int) -> str:
    """Convert minutes to human-readable time ago string."""
    if minutes < 60:
        return f"{minutes}m ago"
    elif minutes < 1440:  # Less than 24 hours
        hours = minutes // 60
        return f"{hours}h ago"
    else:
        days = minutes // 1440
        return f"{days}d ago"


def get_latest_news(count: int = 15, category: str = "all") -> List[Dict]:
    """
    Get the latest transfer portal news.

    Args:
        count: Number of news items to return
        category: Filter by category ('all', 'commitment', 'entry', 'rumor', 'analysis')

    Returns:
        List of news items with timestamps
    """
    # Filter by category if specified
    if category != "all":
        filtered = [n for n in MOCK_NEWS if n["category"] == category]
    else:
        filtered = MOCK_NEWS.copy()

    # Shuffle to simulate different ordering
    random.seed(42)  # Consistent for demo
    random.shuffle(filtered)

    # Add timestamps (mock - in production would be real)
    news_with_time = []
    for i, item in enumerate(filtered[:count]):
        minutes_ago = 5 + (i * 25) + random.randint(0, 15)  # Spread out over time
        news_with_time.append({
            **item,
            "time_ago": get_time_ago(minutes_ago),
            "minutes_ago": minutes_ago,
            "source_color": SOURCE_COLORS.get(item["source"], "#666"),
        })

    return news_with_time


def get_news_categories() -> List[Dict]:
    """Get available news categories with counts."""
    categories = [
        {"id": "all", "label": "All News", "icon": "list"},
        {"id": "commitment", "label": "Commitments", "icon": "checkmark-circle"},
        {"id": "entry", "label": "Portal Entries", "icon": "arrow-right-circle"},
        {"id": "visit", "label": "Official Visits", "icon": "calendar"},
        {"id": "decommit", "label": "De-commits", "icon": "close-circle"},
        {"id": "rumor", "label": "Rumors", "icon": "information-circle"},
        {"id": "analysis", "label": "Analysis", "icon": "bar-chart"},
    ]

    # Add counts
    for cat in categories:
        if cat["id"] == "all":
            cat["count"] = len(MOCK_NEWS)
        else:
            cat["count"] = len([n for n in MOCK_NEWS if n["category"] == cat["id"]])

    return categories


def search_news(query: str) -> List[Dict]:
    """
    Search news by keyword.

    Args:
        query: Search term

    Returns:
        Matching news items
    """
    query = query.lower()
    results = []

    for item in MOCK_NEWS:
        if (query in item["title"].lower() or
            query in item["summary"].lower() or
            query in item["source"].lower()):
            results.append(item)

    return get_latest_news(count=len(results))[:len(results)]
