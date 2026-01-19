"""
NIL or Nothing - Modern Theme for Transfer Portal Dashboard.
Inspired by Linear, Vercel, and Stripe's dashboard aesthetic.
Clean, light, professional design with sports-inspired branding.
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

# Team logos using ESPN CDN
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
    """Return custom CSS for the modern SaaS light theme with NIL or Nothing branding."""
    return f"""
    <style>
        /* Import fonts - Oswald for brand, Playfair Display for serif option, Inter for body */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Oswald:wght@500;600;700&family=Playfair+Display:wght@700;800;900&display=swap');

        /* CSS Variables */
        :root {{
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-brand: 'Playfair Display', Georgia, 'Times New Roman', serif;
            --font-sports: 'Oswald', 'Impact', sans-serif;
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

        /* Hide default Streamlit elements but keep sidebar toggle visible */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Hide header content but keep the sidebar collapse button functional */
        header [data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Ensure sidebar collapse/expand button is always visible */
        [data-testid="collapsedControl"] {{
            visibility: visible !important;
            display: flex !important;
        }}

        /* Main content area */
        .main .block-container {{
            padding: 1rem 3rem 2rem 3rem;
            max-width: 1400px;
        }}

        /* ========== BRAND HEADER ========== */
        .brand-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 0 1.5rem 0;
            border-bottom: 2px solid {COLORS['border']};
            margin-bottom: 1.5rem;
        }}

        .brand-logo {{
            font-family: var(--font-brand);
            font-size: 2rem;
            font-weight: 800;
            color: {COLORS['text_primary']};
            letter-spacing: -0.02em;
            text-transform: uppercase;
        }}

        .brand-logo .accent {{
            color: {COLORS['accent_primary']};
        }}

        .brand-tagline {{
            font-size: 0.75rem;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 0.25rem;
        }}

        /* ========== METRIC CARDS ========== */
        .metric-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-left: 4px solid {COLORS['accent_primary']};
            border-radius: var(--radius-md);
            padding: 1.25rem 1.5rem;
            box-shadow: {COLORS['shadow_sm']};
            transition: all var(--transition-normal);
        }}

        .metric-card:hover {{
            box-shadow: {COLORS['shadow_md']};
            transform: translateY(-2px);
        }}

        .metric-card.success {{
            border-left-color: {COLORS['accent_success']};
        }}

        .metric-card.warning {{
            border-left-color: {COLORS['accent_warning']};
        }}

        .metric-card.info {{
            border-left-color: {COLORS['accent_info']};
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

        /* Custom headers */
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

        /* ========== TEAM TABLE ========== */
        .team-table-container {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .team-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .team-table th {{
            background: {COLORS['bg_secondary']};
            padding: 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 600;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 1px solid {COLORS['border']};
            cursor: pointer;
            user-select: none;
        }}

        .team-table th:hover {{
            background: {COLORS['border_light']};
        }}

        .team-table th .sort-arrow {{
            margin-left: 0.5rem;
            opacity: 0.5;
        }}

        .team-table th.sorted .sort-arrow {{
            opacity: 1;
        }}

        .team-table td {{
            padding: 0.875rem 1rem;
            font-size: 0.875rem;
            color: {COLORS['text_primary']};
            border-bottom: 1px solid {COLORS['border_light']};
            vertical-align: middle;
        }}

        .team-table tr:hover td {{
            background: {COLORS['bg_card_hover']};
        }}

        .team-table tr:last-child td {{
            border-bottom: none;
        }}

        .team-table .team-cell {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .team-table .team-logo {{
            width: 32px;
            height: 32px;
            object-fit: contain;
        }}

        .team-table .team-name {{
            font-weight: 600;
        }}

        .team-table .score-cell {{
            font-weight: 700;
            font-size: 1rem;
        }}

        .team-table .score-positive {{
            color: {COLORS['accent_success']};
        }}

        .team-table .score-negative {{
            color: {COLORS['accent_danger']};
        }}

        .team-table .nil-cell {{
            font-weight: 600;
            color: {COLORS['accent_primary']};
        }}

        .team-table .players-cell {{
            font-size: 0.8125rem;
        }}

        .team-table .conf-cell {{
            background: {COLORS['bg_secondary']};
            padding: 0.25rem 0.625rem;
            border-radius: var(--radius-full);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            display: inline-block;
        }}

        /* ========== SIDEBAR ========== */
        [data-testid="stSidebar"] {{
            background: {COLORS['bg_sidebar']};
            border-right: 1px solid {COLORS['border']};
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding: 1.5rem 1.25rem;
        }}

        /* Hide Streamlit's default page navigation (we use custom nav with icons) */
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}

        /* ========== DATA TABLE ========== */
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
            cursor: pointer;
        }}

        .data-table th:hover {{
            background: {COLORS['border_light']};
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
        }}

        .player-class {{
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_secondary']};
            padding: 0.25rem 0.5rem;
            border-radius: var(--radius-sm);
            font-size: 0.6875rem;
            font-weight: 500;
        }}

        .player-value {{
            font-weight: 600;
            color: {COLORS['accent_success']};
            font-size: 0.875rem;
        }}

        /* Badges */
        .inflow-badge {{
            background: {COLORS['accent_success']}15;
            color: {COLORS['accent_success']};
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-full);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .outflow-badge {{
            background: {COLORS['chart_negative']}15;
            color: {COLORS['chart_negative']};
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-full);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
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

        /* ========== NEWS FEED ========== */
        .news-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-md);
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            transition: all var(--transition-fast);
        }}

        .news-card:hover {{
            border-color: {COLORS['accent_info']};
            box-shadow: {COLORS['shadow_md']};
        }}

        .news-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }}

        .news-source {{
            font-size: 0.6875rem;
            color: {COLORS['accent_info']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}

        .news-time {{
            font-size: 0.75rem;
            color: {COLORS['text_muted']};
        }}

        .news-title {{
            font-size: 1rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }}

        .news-summary {{
            font-size: 0.875rem;
            color: {COLORS['text_secondary']};
            line-height: 1.6;
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid {COLORS['border_light']};
        }}

        .news-reporter {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.75rem;
            color: {COLORS['text_muted']};
        }}

        /* ========== METHODOLOGY CARD ========== */
        .methodology-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .formula-display {{
            background: {COLORS['bg_secondary']};
            border: 1px solid {COLORS['border']};
            border-radius: var(--radius-md);
            padding: 1.5rem 2rem;
            margin: 1.5rem 0;
            text-align: center;
        }}

        .formula-display .formula {{
            font-family: 'Times New Roman', Georgia, serif;
            font-size: 1.25rem;
            font-style: italic;
            color: {COLORS['text_primary']};
            line-height: 2;
        }}

        .formula-display .formula-part {{
            display: block;
            margin: 0.5rem 0;
        }}

        .position-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}

        .position-table th {{
            background: {COLORS['bg_secondary']};
            padding: 0.875rem 1rem;
            text-align: left;
            font-size: 0.75rem;
            font-weight: 600;
            color: {COLORS['text_muted']};
            text-transform: uppercase;
            border-bottom: 2px solid {COLORS['border']};
        }}

        .position-table td {{
            padding: 1rem;
            border-bottom: 1px solid {COLORS['border_light']};
            vertical-align: top;
        }}

        .position-table td:first-child {{
            font-weight: 600;
            color: {COLORS['accent_primary']};
            width: 80px;
        }}

        .position-table td:nth-child(2) {{
            font-weight: 700;
            color: {COLORS['text_primary']};
            width: 100px;
        }}

        .position-table td:last-child {{
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            line-height: 1.6;
        }}

        /* ========== MISC ========== */
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

        /* Sample data banner */
        .sample-data-banner {{
            background: {COLORS['accent_warning']}15;
            border: 1px solid {COLORS['accent_warning']}30;
            border-radius: var(--radius-sm);
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8125rem;
            color: {COLORS['accent_warning']};
        }}

        /* Loading state */
        .loading-spinner {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 3rem;
        }}
    </style>
    """


def render_brand_header():
    """Render the NIL or Nothing brand header."""
    return f"""
    <div class="brand-header">
        <div>
            <div class="brand-logo">NIL <span class="accent">or</span> Nothing</div>
            <div class="brand-tagline">Transfer Portal Analytics • 2026 Offseason</div>
        </div>
    </div>
    """


def render_metric_card(value, label, variant="default", icon=""):
    """Render a styled metric card."""
    variant_class = f" {variant}" if variant != "default" else ""
    return f"""
    <div class="metric-card{variant_class}">
        <p class="metric-value">{icon}{value}</p>
        <p class="metric-label">{label}</p>
    </div>
    """


def render_team_row(rank, team, logo_url, score, nil_spent, off_players, def_players, conference):
    """Render a team row for the rankings table."""
    score_class = "score-positive" if score >= 0 else "score-negative"
    score_prefix = "+" if score >= 0 else ""

    return f"""
    <tr>
        <td style="font-weight: 600; color: {COLORS['text_muted']};">{rank}</td>
        <td>
            <div class="team-cell">
                <img src="{logo_url}" class="team-logo" alt="{team}" />
                <span class="team-name">{team}</span>
            </div>
        </td>
        <td class="score-cell {score_class}">{score_prefix}{score:.1f}</td>
        <td class="nil-cell">${nil_spent:.1f}M</td>
        <td class="players-cell">{off_players}</td>
        <td class="players-cell">{def_players}</td>
        <td><span class="conf-cell">{conference}</span></td>
    </tr>
    """


def render_player_row(name, position, player_class, school, value, score, flow_type="inflow"):
    """Render a styled player row with class field."""
    badge_class = "inflow-badge" if flow_type == "inflow" else "outflow-badge"
    badge_text = "IN" if flow_type == "inflow" else "OUT"
    return f"""
    <div class="player-row">
        <span class="{badge_class}">{badge_text}</span>
        <span class="player-name">{name}</span>
        <span class="player-position">{position}</span>
        <span class="player-class">{player_class}</span>
        <span style="color: {COLORS['text_muted']}; font-size: 0.8125rem;">{school}</span>
        <span class="player-value">${value:.2f}M</span>
    </div>
    """


def render_news_card(title, summary, source, reporter, time_ago, category):
    """Render a news card for the live feed."""
    category_colors = {
        "commitment": COLORS["accent_success"],
        "entry": COLORS["accent_warning"],
        "visit": COLORS["accent_info"],
        "rumor": COLORS["accent_secondary"],
    }
    cat_color = category_colors.get(category.lower(), COLORS["text_muted"])

    return f"""
    <div class="news-card">
        <div class="news-header">
            <span class="news-source" style="color: {cat_color};">{category.upper()}</span>
            <span class="news-time">{time_ago}</span>
        </div>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{summary}</p>
        <div class="news-meta">
            <span class="news-reporter">📰 {reporter} • {source}</span>
        </div>
    </div>
    """


def render_sample_data_banner():
    """Render a banner indicating sample data is being used."""
    return f"""
    <div class="sample-data-banner">
        ⚠️ <strong>Sample Data:</strong> This dashboard displays simulated data for demonstration. Real-time data would require API integration with 247Sports, On3, or ESPN.
    </div>
    """


def get_team_logo(team_name: str) -> str:
    """Get the logo URL for a team."""
    return TEAM_LOGOS.get(team_name, "")
