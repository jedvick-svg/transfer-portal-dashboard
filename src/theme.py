"""
Modern SaaS theme for the Transfer Portal Dashboard.
Inspired by Linear, Vercel, and Stripe's dashboard aesthetic.
Clean, light, professional design with generous whitespace.
"""

# Modern SaaS color palette - light theme with professional accents
COLORS = {
    # Primary backgrounds
    "bg_primary": "#ffffff",
    "bg_secondary": "#f8fafc",
    "bg_card": "#ffffff",
    "bg_card_hover": "#f8fafc",
    "bg_sidebar": "#f1f5f9",

    # Accent colors - Professional blues/purples
    "accent_primary": "#6366f1",  # Indigo
    "accent_secondary": "#8b5cf6",  # Purple
    "accent_success": "#0d9488",  # Teal
    "accent_warning": "#f59e0b",  # Amber
    "accent_danger": "#ef4444",  # Red
    "accent_info": "#0ea5e9",  # Sky blue

    # Data visualization colors
    "chart_positive": "#0d9488",  # Teal
    "chart_negative": "#f97316",  # Orange (softer than red)
    "chart_primary": "#6366f1",
    "chart_secondary": "#8b5cf6",
    "chart_tertiary": "#0ea5e9",

    # Text colors
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",

    # Borders and dividers
    "border": "#e2e8f0",
    "border_light": "#f1f5f9",
    "divider": "#e2e8f0",

    # Shadows
    "shadow_sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
    "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
}

# Team colors for the major programs
TEAM_COLORS = {
    "Georgia": {"primary": "#BA0C2F", "secondary": "#000000"},
    "Alabama": {"primary": "#9E1B32", "secondary": "#828A8F"},
    "Ohio State": {"primary": "#BB0000", "secondary": "#666666"},
    "Texas": {"primary": "#BF5700", "secondary": "#333F48"},
    "Oregon": {"primary": "#154733", "secondary": "#FEE123"},
    "Penn State": {"primary": "#041E42", "secondary": "#FFFFFF"},
    "Michigan": {"primary": "#00274C", "secondary": "#FFCB05"},
    "Notre Dame": {"primary": "#0C2340", "secondary": "#C99700"},
    "LSU": {"primary": "#461D7C", "secondary": "#FDD023"},
    "USC": {"primary": "#990000", "secondary": "#FFC72C"},
    "Florida State": {"primary": "#782F40", "secondary": "#CEB888"},
    "Clemson": {"primary": "#F56600", "secondary": "#522D80"},
    "Tennessee": {"primary": "#FF8200", "secondary": "#58595B"},
    "Oklahoma": {"primary": "#841617", "secondary": "#FDF9D8"},
    "Miami": {"primary": "#F47321", "secondary": "#005030"},
    "Florida": {"primary": "#0021A5", "secondary": "#FA4616"},
    "Auburn": {"primary": "#0C2340", "secondary": "#E87722"},
    "Texas A&M": {"primary": "#500000", "secondary": "#FFFFFF"},
    "Wisconsin": {"primary": "#C5050C", "secondary": "#FFFFFF"},
    "Ole Miss": {"primary": "#CE1126", "secondary": "#14213D"},
    "Colorado": {"primary": "#CFB87C", "secondary": "#000000"},
    "South Carolina": {"primary": "#73000A", "secondary": "#000000"},
    "Kentucky": {"primary": "#0033A0", "secondary": "#FFFFFF"},
    "Arizona": {"primary": "#CC0033", "secondary": "#003366"},
    "Missouri": {"primary": "#F1B82D", "secondary": "#000000"},
}

# Team logos using ESPN CDN (reliable, high-quality logos)
TEAM_LOGOS = {
    "Georgia": "https://a.espncdn.com/i/teamlogos/ncaa/500/61.png",
    "Alabama": "https://a.espncdn.com/i/teamlogos/ncaa/500/333.png",
    "Ohio State": "https://a.espncdn.com/i/teamlogos/ncaa/500/194.png",
    "Texas": "https://a.espncdn.com/i/teamlogos/ncaa/500/251.png",
    "Oregon": "https://a.espncdn.com/i/teamlogos/ncaa/500/2483.png",
    "Penn State": "https://a.espncdn.com/i/teamlogos/ncaa/500/213.png",
    "Michigan": "https://a.espncdn.com/i/teamlogos/ncaa/500/130.png",
    "Notre Dame": "https://a.espncdn.com/i/teamlogos/ncaa/500/87.png",
    "LSU": "https://a.espncdn.com/i/teamlogos/ncaa/500/99.png",
    "USC": "https://a.espncdn.com/i/teamlogos/ncaa/500/30.png",
    "Florida State": "https://a.espncdn.com/i/teamlogos/ncaa/500/52.png",
    "Clemson": "https://a.espncdn.com/i/teamlogos/ncaa/500/228.png",
    "Tennessee": "https://a.espncdn.com/i/teamlogos/ncaa/500/2633.png",
    "Oklahoma": "https://a.espncdn.com/i/teamlogos/ncaa/500/201.png",
    "Miami": "https://a.espncdn.com/i/teamlogos/ncaa/500/2390.png",
    "Florida": "https://a.espncdn.com/i/teamlogos/ncaa/500/57.png",
    "Auburn": "https://a.espncdn.com/i/teamlogos/ncaa/500/2.png",
    "Texas A&M": "https://a.espncdn.com/i/teamlogos/ncaa/500/245.png",
    "Wisconsin": "https://a.espncdn.com/i/teamlogos/ncaa/500/275.png",
    "Ole Miss": "https://a.espncdn.com/i/teamlogos/ncaa/500/145.png",
    "Colorado": "https://a.espncdn.com/i/teamlogos/ncaa/500/38.png",
    "South Carolina": "https://a.espncdn.com/i/teamlogos/ncaa/500/2579.png",
    "Kentucky": "https://a.espncdn.com/i/teamlogos/ncaa/500/96.png",
    "Arizona": "https://a.espncdn.com/i/teamlogos/ncaa/500/12.png",
    "Missouri": "https://a.espncdn.com/i/teamlogos/ncaa/500/142.png",
}


def get_team_logo(team_name: str) -> str:
    """Get the logo URL for a team."""
    return TEAM_LOGOS.get(team_name, "")


def get_custom_css():
    """Return custom CSS for the modern SaaS light theme."""
    return f"""
    <style>
        /* Import modern fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* CSS Variables for easy theming */
        :root {{
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --radius-full: 9999px;
            --transition-fast: 150ms ease;
            --transition-normal: 200ms ease;
        }}

        /* Global styles */
        .stApp {{
            background: {COLORS['bg_secondary']};
            font-family: var(--font-sans);
        }}

        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* Main content area - add padding for top nav */
        .main .block-container {{
            padding: 1rem 3rem 2rem 3rem;
            max-width: 1400px;
        }}

        /* ========== TOP NAVIGATION BAR ========== */
        .top-nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 56px;
            background: {COLORS['bg_primary']};
            border-bottom: 1px solid {COLORS['border']};
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            z-index: 1000;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .top-nav-brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 700;
            font-size: 1.125rem;
            color: {COLORS['text_primary']};
        }}

        .top-nav-links {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .top-nav-link {{
            padding: 0.5rem 1rem;
            border-radius: var(--radius-sm);
            font-size: 0.875rem;
            font-weight: 500;
            color: {COLORS['text_secondary']};
            text-decoration: none;
            transition: all var(--transition-fast);
        }}

        .top-nav-link:hover {{
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
        }}

        .top-nav-link.active {{
            background: {COLORS['accent_primary']}15;
            color: {COLORS['accent_primary']};
        }}

        /* Spacer for fixed top nav */
        .nav-spacer {{
            height: 56px;
        }}

        /* ========== CLICKABLE STAT CARDS ========== */
        .metric-card-link {{
            text-decoration: none;
            display: block;
        }}

        .metric-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-left: 4px solid {COLORS['accent_primary']};
            border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            box-shadow: {COLORS['shadow_sm']};
            transition: all var(--transition-normal);
            cursor: pointer;
        }}

        .metric-card:hover {{
            box-shadow: {COLORS['shadow_md']};
            transform: translateY(-3px);
            border-color: {COLORS['accent_primary']};
        }}

        .metric-card.success {{
            border-left-color: {COLORS['accent_success']};
        }}
        .metric-card.success:hover {{
            border-color: {COLORS['accent_success']};
        }}

        .metric-card.warning {{
            border-left-color: {COLORS['accent_warning']};
        }}
        .metric-card.warning:hover {{
            border-color: {COLORS['accent_warning']};
        }}

        .metric-card.info {{
            border-left-color: {COLORS['accent_info']};
        }}
        .metric-card.info:hover {{
            border-color: {COLORS['accent_info']};
        }}

        .metric-value {{
            font-size: 1.875rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin: 0;
            line-height: 1.2;
        }}

        .metric-label {{
            font-size: 0.8125rem;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 500;
            margin-top: 0.375rem;
        }}

        /* Custom header */
        .main-header {{
            font-size: 2.25rem;
            font-weight: 800;
            color: {COLORS['text_primary']};
            margin-bottom: 0.25rem;
            letter-spacing: -0.03em;
            line-height: 1.2;
        }}

        .sub-header {{
            color: {COLORS['text_secondary']};
            font-size: 1.125rem;
            font-weight: 400;
            margin-bottom: 1.5rem;
            line-height: 1.5;
        }}

        /* ========== CLICKABLE TEAM CARDS ========== */
        .team-card-link {{
            text-decoration: none;
            display: block;
        }}

        .team-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            margin-bottom: 0.5rem;
            transition: all var(--transition-fast);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .team-card:hover {{
            background: {COLORS['bg_card_hover']};
            border-color: {COLORS['accent_primary']};
            box-shadow: {COLORS['shadow_md']};
            transform: translateX(4px);
        }}

        .team-logo {{
            width: 40px;
            height: 40px;
            border-radius: var(--radius-sm);
            object-fit: contain;
            background: {COLORS['bg_secondary']};
            padding: 4px;
        }}

        .team-rank {{
            font-size: 0.875rem;
            font-weight: 600;
            color: {COLORS['text_muted']};
            min-width: 1.75rem;
        }}

        .team-info {{
            flex: 1;
            min-width: 0;
        }}

        .team-name {{
            font-size: 0.9375rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 0;
            line-height: 1.3;
        }}

        .team-conference {{
            font-size: 0.75rem;
            color: {COLORS['text_muted']};
            margin-top: 0.125rem;
        }}

        .team-stats {{
            text-align: right;
            flex-shrink: 0;
        }}

        .team-value {{
            font-size: 0.9375rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
        }}

        .team-net {{
            font-size: 0.75rem;
            font-weight: 500;
            margin-top: 0.125rem;
        }}

        .team-net.positive {{
            color: {COLORS['accent_success']};
        }}

        .team-net.negative {{
            color: {COLORS['accent_danger']};
        }}

        /* ========== SIDEBAR IMPROVEMENTS ========== */
        [data-testid="stSidebar"] {{
            background: {COLORS['bg_sidebar']};
            border-right: 1px solid {COLORS['border']};
            transition: all 0.3s ease;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding: 1.5rem 1.25rem;
        }}

        /* Sidebar collapse button styling */
        [data-testid="stSidebar"] [data-testid="collapsedControl"] {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-sm);
            color: {COLORS['text_secondary']};
        }}

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stRadio label {{
            color: {COLORS['text_secondary']};
            font-weight: 500;
            font-size: 0.8125rem;
        }}

        /* ========== BACK BUTTON ========== */
        .back-button {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-sm);
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            font-weight: 500;
            text-decoration: none;
            transition: all var(--transition-fast);
            cursor: pointer;
            margin-bottom: 1.5rem;
        }}

        .back-button:hover {{
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border-color: {COLORS['accent_primary']};
        }}

        /* ========== DATA TABLE STYLES ========== */
        .data-table-container {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th {{
            background: {COLORS['bg_secondary']};
            padding: 0.875rem 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 600;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid {COLORS['border']};
        }}

        .data-table td {{
            padding: 0.875rem 1rem;
            font-size: 0.875rem;
            color: {COLORS['text_primary']};
            border-bottom: 1px solid {COLORS['border_light']};
        }}

        .data-table tr:hover td {{
            background: {COLORS['bg_card_hover']};
        }}

        .data-table tr:last-child td {{
            border-bottom: none;
        }}

        /* ========== PLAYER ROWS ========== */
        .player-row {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-sm);
            padding: 0.875rem 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.875rem;
            transition: all var(--transition-fast);
        }}

        .player-row:hover {{
            background: {COLORS['bg_card_hover']};
        }}

        .player-name {{
            font-weight: 500;
            color: {COLORS['text_primary']};
            flex: 1;
            font-size: 0.875rem;
        }}

        .player-position {{
            background: {COLORS['accent_primary']}15;
            color: {COLORS['accent_primary']};
            padding: 0.25rem 0.625rem;
            border-radius: var(--radius-sm);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }}

        .player-value {{
            font-weight: 600;
            color: {COLORS['accent_success']};
            font-size: 0.875rem;
        }}

        /* Inflow/Outflow badges */
        .inflow-badge {{
            background: {COLORS['accent_success']}15;
            color: {COLORS['accent_success']};
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-full);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .outflow-badge {{
            background: {COLORS['chart_negative']}15;
            color: {COLORS['chart_negative']};
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-full);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        /* ========== SECTION HEADERS ========== */
        .section-header {{
            font-size: 1.125rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 1.5rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        /* ========== FILTER BAR ========== */
        .filter-bar {{
            display: flex;
            gap: 1rem;
            padding: 1rem;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-md);
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            align-items: flex-end;
        }}

        .filter-item {{
            flex: 1;
            min-width: 150px;
        }}

        .filter-label {{
            font-size: 0.75rem;
            font-weight: 500;
            color: {COLORS['text_muted']};
            margin-bottom: 0.375rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        /* ========== NEWS ITEMS ========== */
        .news-item {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-md);
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            transition: all var(--transition-fast);
        }}

        .news-item:hover {{
            border-color: {COLORS['accent_info']};
            box-shadow: {COLORS['shadow_sm']};
        }}

        .news-source {{
            font-size: 0.6875rem;
            color: {COLORS['accent_info']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        .news-title {{
            font-size: 0.9375rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }}

        .news-time {{
            font-size: 0.75rem;
            color: {COLORS['text_muted']};
        }}

        /* ========== CARD CONTAINERS ========== */
        .card-container {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            box-shadow: {COLORS['shadow_sm']};
        }}

        /* ========== METHODOLOGY ========== */
        .methodology-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .formula-box {{
            background: {COLORS['bg_secondary']};
            border: 1px solid {COLORS['border']};
            border-left: 3px solid {COLORS['accent_primary']};
            border-radius: var(--radius-sm);
            padding: 1.25rem;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            color: {COLORS['text_primary']};
            font-size: 0.875rem;
            margin: 1rem 0;
        }}

        /* ========== MISC ========== */
        .stDataFrame {{
            background: {COLORS['bg_card']};
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid {COLORS['border']};
        }}

        .stButton > button {{
            background: {COLORS['accent_primary']};
            color: white;
            border: none;
            border-radius: var(--radius-sm);
            padding: 0.5rem 1.25rem;
            font-weight: 500;
            font-size: 0.875rem;
            transition: all var(--transition-fast);
        }}

        .stButton > button:hover {{
            background: {COLORS['accent_secondary']};
            box-shadow: {COLORS['shadow_sm']};
        }}

        .stTabs [data-baseweb="tab-list"] {{
            background: {COLORS['bg_card']};
            border-radius: var(--radius-md);
            padding: 0.25rem;
            gap: 0.25rem;
            border: 1px solid {COLORS['border']};
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            color: {COLORS['text_secondary']};
            border-radius: var(--radius-sm);
            padding: 0.5rem 1rem;
            font-weight: 500;
            font-size: 0.875rem;
        }}

        .stTabs [aria-selected="true"] {{
            background: {COLORS['accent_primary']};
            color: white;
        }}

        hr {{
            border: none;
            border-top: 1px solid {COLORS['divider']};
            margin: 1.5rem 0;
        }}

        a {{
            color: {COLORS['accent_primary']};
            text-decoration: none;
            font-weight: 500;
        }}

        a:hover {{
            color: {COLORS['accent_secondary']};
        }}

        .value-positive {{
            color: {COLORS['accent_success']};
        }}

        .value-negative {{
            color: {COLORS['accent_danger']};
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}

        ::-webkit-scrollbar-track {{
            background: transparent;
        }}

        ::-webkit-scrollbar-thumb {{
            background: {COLORS['border']};
            border-radius: 3px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['text_muted']};
        }}

        .stSelectbox > div > div {{
            background: {COLORS['bg_card']};
            border-color: {COLORS['border']};
            border-radius: var(--radius-sm);
        }}

        .stTextInput > div > div > input {{
            background: {COLORS['bg_card']};
            border-color: {COLORS['border']};
            border-radius: var(--radius-sm);
            color: {COLORS['text_primary']};
        }}

        .empty-state {{
            text-align: center;
            padding: 3rem 2rem;
            color: {COLORS['text_muted']};
        }}

        .empty-state-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }}

        /* Loading spinner */
        .loading-spinner {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 3rem;
        }}

        /* Pagination */
        .pagination {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 1.5rem;
        }}

        .pagination-btn {{
            padding: 0.5rem 1rem;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-sm);
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            cursor: pointer;
            transition: all var(--transition-fast);
        }}

        .pagination-btn:hover {{
            background: {COLORS['bg_secondary']};
            border-color: {COLORS['accent_primary']};
        }}

        .pagination-btn.active {{
            background: {COLORS['accent_primary']};
            color: white;
            border-color: {COLORS['accent_primary']};
        }}
    </style>
    """


def render_top_nav(active_page="home"):
    """Render the top navigation bar."""
    nav_items = [
        {"id": "home", "label": "Home", "url": "/"},
        {"id": "database", "label": "Database", "url": "/Database"},
        {"id": "teams", "label": "Teams", "url": "/Team_Details"},
        {"id": "about", "label": "About", "url": "/About"},
    ]

    links_html = ""
    for item in nav_items:
        active_class = "active" if item["id"] == active_page else ""
        links_html += f'<a href="{item["url"]}" class="top-nav-link {active_class}">{item["label"]}</a>'

    return f"""
    <div class="top-nav">
        <div class="top-nav-brand">
            <span>🏈</span>
            <span>Transfer Portal</span>
        </div>
        <div class="top-nav-links">
            {links_html}
        </div>
    </div>
    <div class="nav-spacer"></div>
    """


def render_metric_card_clickable(value, label, variant="default", link="/Database"):
    """Render a clickable styled metric card."""
    variant_class = f" {variant}" if variant != "default" else ""
    return f"""
    <a href="{link}" class="metric-card-link">
        <div class="metric-card{variant_class}">
            <p class="metric-value">{value}</p>
            <p class="metric-label">{label}</p>
        </div>
    </a>
    """


def render_metric_card(value, label, variant="default", icon=""):
    """Render a styled metric card with optional variant for border color."""
    variant_class = f" {variant}" if variant != "default" else ""
    return f"""
    <div class="metric-card{variant_class}">
        <p class="metric-value">{icon}{value}</p>
        <p class="metric-label">{label}</p>
    </div>
    """


def render_team_card_clickable(rank, team, conference, value, net_value, logo_url=""):
    """Render a clickable styled team card with logo."""
    net_class = "positive" if net_value >= 0 else "negative"
    net_prefix = "+" if net_value >= 0 else ""
    logo_html = f'<img src="{logo_url}" class="team-logo" alt="{team}" />' if logo_url else ""
    team_url = team.replace(" ", "_")

    return f"""
    <a href="/Team_Details?team={team_url}" class="team-card-link">
        <div class="team-card">
            <span class="team-rank">{rank}</span>
            {logo_html}
            <div class="team-info">
                <div class="team-name">{team}</div>
                <div class="team-conference">{conference}</div>
            </div>
            <div class="team-stats">
                <div class="team-value">${value:.1f}M</div>
                <div class="team-net {net_class}">{net_prefix}${net_value:.1f}M</div>
            </div>
        </div>
    </a>
    """


def render_team_card(rank, team, conference, value, net_value, logo_url=""):
    """Render a styled team card with logo (non-clickable version)."""
    net_class = "positive" if net_value >= 0 else "negative"
    net_prefix = "+" if net_value >= 0 else ""
    logo_html = f'<img src="{logo_url}" class="team-logo" alt="{team}" />' if logo_url else ""

    return f"""
    <div class="team-card">
        <span class="team-rank">{rank}</span>
        {logo_html}
        <div class="team-info">
            <div class="team-name">{team}</div>
            <div class="team-conference">{conference}</div>
        </div>
        <div class="team-stats">
            <div class="team-value">${value:.1f}M</div>
            <div class="team-net {net_class}">{net_prefix}${net_value:.1f}M</div>
        </div>
    </div>
    """


def render_back_button(url="/", label="Back to Dashboard"):
    """Render a back button."""
    return f"""
    <a href="{url}" class="back-button">
        ← {label}
    </a>
    """


def render_player_row(name, position, school, value, flow_type="inflow"):
    """Render a styled player row."""
    badge_class = "inflow-badge" if flow_type == "inflow" else "outflow-badge"
    badge_text = "IN" if flow_type == "inflow" else "OUT"
    return f"""
    <div class="player-row">
        <span class="{badge_class}">{badge_text}</span>
        <span class="player-name">{name}</span>
        <span class="player-position">{position}</span>
        <span style="color: {COLORS['text_muted']}; font-size: 0.8125rem;">{school}</span>
        <span class="player-value">${value:.2f}M</span>
    </div>
    """


def render_news_item(source, title, time_ago, url="#"):
    """Render a styled news item."""
    return f"""
    <div class="news-item">
        <div class="news-source">{source}</div>
        <div class="news-title">{title}</div>
        <div class="news-time">{time_ago}</div>
    </div>
    """
