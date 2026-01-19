"""
Team Details Page - NIL or Nothing

Shows detailed inflows and outflows for a selected team,
including player valuations, scoring breakdown, and transfer history.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.theme import get_custom_css, COLORS, TEAM_COLORS, get_team_logo, render_brand_header, render_sample_data_banner
from src.data import get_all_teams_list, get_team_details, get_team_conference

# Page configuration
st.set_page_config(
    page_title="Team Details | NIL or Nothing",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Brand header
st.markdown(render_brand_header(), unsafe_allow_html=True)

# Get query params for direct linking
params = st.query_params
default_team = params.get("team", "Georgia")
# Handle URL-encoded team names (replace underscores with spaces)
if default_team:
    default_team = default_team.replace("_", " ")

# Navigation
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 800; color: {COLORS['text_primary']}; text-transform: uppercase;">
                NIL <span style="color: {COLORS['accent_primary']};">or</span> Nothing
            </div>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']}; margin-top: 0.25rem;">2026 Transfer Portal</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")
    st.page_link("app.py", label="🏠 Home", icon=None)
    st.page_link("pages/1_Team_Details.py", label="📋 Teams", icon=None)
    st.page_link("pages/4_Database.py", label="📊 Database", icon=None)
    st.page_link("pages/3_Live_Feed.py", label="📰 News", icon=None)
    st.page_link("pages/5_About.py", label="ℹ️ About", icon=None)

    st.markdown("---")

    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em;">Select Team</p>
        </div>
    """, unsafe_allow_html=True)

    teams = get_all_teams_list()

    # Safely get default team index
    try:
        default_index = teams.index(default_team) if default_team in teams else 0
    except (ValueError, IndexError):
        default_index = 0

    selected_team = st.selectbox(
        "Team",
        teams,
        index=default_index,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div style="color: {COLORS['text_muted']}; font-size: 0.6875rem; line-height: 1.5;">
            <p style="margin-bottom: 0.25rem;">Last updated: Jan 18, 2026</p>
            <p>Data: 247Sports, ESPN, On3</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main content team selector (more prominent)
st.markdown(f"""
    <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; box-shadow: {COLORS['shadow_sm']};">
        <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem; margin-bottom: 0.75rem;">Search or select a team to view their transfer portal activity:</p>
    </div>
""", unsafe_allow_html=True)

col_search, col_spacer = st.columns([2, 3])
with col_search:
    # Searchable team selector in main content
    selected_team = st.selectbox(
        "Choose a team",
        teams,
        index=default_index,
        key="main_team_selector",
        help="Type to search or scroll to select"
    )

# Get team data with error handling
try:
    team_data = get_team_details(selected_team)
except Exception as e:
    team_data = None
    st.error(f"Error loading team data: {str(e)}")

if not team_data:
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">🏈</div>
            <p style="font-size: 1rem; color: {COLORS['text_secondary']}; margin-bottom: 0.25rem;">Team not found</p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.875rem;">Please select a valid team from the sidebar</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

info = team_data["info"]
conference = team_data["conference"]
inflows = team_data["inflows"]
outflows = team_data["outflows"]
score_data = team_data.get("score_data", {})

# Get team colors and logo
team_colors = TEAM_COLORS.get(selected_team, {"primary": COLORS["accent_primary"], "secondary": COLORS["text_secondary"]})
logo_url = get_team_logo(selected_team)

# Sample data notice
st.markdown(render_sample_data_banner(), unsafe_allow_html=True)

# Header with team branding and logo
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 2rem;">
        <div style="
            width: 80px;
            height: 80px;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px;
            box-shadow: {COLORS['shadow_md']};
        ">
            <img src="{logo_url}" style="width: 100%; height: 100%; object-fit: contain;" alt="{selected_team}" />
        </div>
        <div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <h1 class="main-header" style="margin: 0;">{selected_team}</h1>
                <span style="
                    background: {team_colors['primary']}15;
                    color: {team_colors['primary']};
                    padding: 0.25rem 0.75rem;
                    border-radius: 9999px;
                    font-size: 0.75rem;
                    font-weight: 600;
                ">#{info['rank']}</span>
            </div>
            <p style="color: {COLORS['text_secondary']}; margin: 0.25rem 0 0 0; font-size: 1rem;">{conference}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Summary metrics - now using Score
col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

team_score = info.get("score", score_data.get("total_score", 0))
nil_spent = info.get("nil_spent", 0)
offensive_net = info.get("offensive_net", score_data.get("offensive_net", 0))
defensive_net = info.get("defensive_net", score_data.get("defensive_net", 0))

with col1:
    score_color = COLORS['accent_success'] if team_score >= 0 else COLORS['accent_danger']
    score_prefix = "+" if team_score >= 0 else ""
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {score_color};">
            <p class="metric-value" style="color: {score_color};">{score_prefix}{team_score:.1f}</p>
            <p class="metric-label">Net Score</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card success">
            <p class="metric-value">{info['inflows']}</p>
            <p class="metric-label">Players In</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {COLORS['chart_negative']};">
            <p class="metric-value">{info['outflows']}</p>
            <p class="metric-label">Players Out</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card info">
            <p class="metric-value">${nil_spent:.1f}M</p>
            <p class="metric-label">NIL Spent</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    off_color = COLORS['accent_success'] if offensive_net >= 0 else COLORS['chart_negative']
    def_color = COLORS['accent_success'] if defensive_net >= 0 else COLORS['chart_negative']
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: {off_color}; font-weight: 600; font-size: 0.875rem;">OFF: {'+' if offensive_net >= 0 else ''}{offensive_net:.1f}</span>
                <span style="color: {def_color}; font-weight: 600; font-size: 0.875rem;">DEF: {'+' if defensive_net >= 0 else ''}{defensive_net:.1f}</span>
            </div>
            <p class="metric-label">Position Net Scores</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Tabs for Inflows and Outflows
tab1, tab2 = st.tabs(["Portal Inflows", "Portal Outflows"])

with tab1:
    st.markdown(
        f'<div class="section-header">Players Gained <span style="color: {COLORS["accent_success"]}; font-weight: 500;">({len(inflows)})</span></div>',
        unsafe_allow_html=True
    )

    if inflows:
        # Sort by score
        inflows_sorted = sorted(inflows, key=lambda x: x.get("score", 0), reverse=True)

        for player in inflows_sorted:
            hs_display = f"{player['hs_rating']:.4f}" if player.get('hs_rating') else "N/A"
            games_display = f"{player['games_played']} games" if player.get('games_played', 0) > 0 else "Freshman"
            from_team = player.get("previous_team", "Unknown")
            player_score = player.get("score", 0)
            player_class = player.get("player_class", "Unknown")

            st.markdown(
                f"""
                <div class="player-row" style="border-left: 3px solid {COLORS['accent_success']};">
                    <span class="inflow-badge">IN</span>
                    <span class="player-name" style="min-width: 140px;">{player['name']}</span>
                    <span class="player-position">{player['position']}</span>
                    <span class="player-class">{player_class}</span>
                    <div style="flex: 1; display: flex; gap: 1.5rem; color: {COLORS['text_muted']}; font-size: 0.8125rem;">
                        <span>From: <strong style="color: {COLORS['text_secondary']};">{from_team}</strong></span>
                        <span>HS: {hs_display}</span>
                        <span>{games_display}</span>
                    </div>
                    <span style="color: {COLORS['accent_success']}; font-weight: 600; margin-right: 0.5rem;">+{player_score:.1f}</span>
                    <span class="player-value">${player['value']:.2f}M</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expandable details
            with st.expander(f"Value breakdown for {player['name']}", expanded=False):
                breakdown = player.get("value_breakdown", {})
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown(f"**Input Data**")
                    st.markdown(f"- HS Rating: `{breakdown.get('hs_rating', 'N/A')}`")
                    st.markdown(f"- HS Normalized: `{breakdown.get('hs_normalized', 'N/A')}`")
                    st.markdown(f"- Stats Percentile: `{breakdown.get('stats_percentile', 'N/A')}`")
                    st.markdown(f"- Player Class: `{player_class}`")

                with col_b:
                    st.markdown(f"**Calculation**")
                    st.markdown(f"- HS Weight: `{breakdown.get('hs_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Stats Weight: `{breakdown.get('stats_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Position Multiplier: `{breakdown.get('position_multiplier', 1)}x`")
                    st.markdown(f"- Class Weight: `{breakdown.get('class_weight', 1)}x`")
                    st.markdown(f"- **Score: `{player_score:.1f}`**")
                    st.markdown(f"- **Value: `${breakdown.get('final_value', 0):.2f}M`**")
    else:
        st.markdown(
            f"""
            <div class="empty-state">
                <div class="empty-state-icon">📥</div>
                <p>No inflows recorded for this team.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab2:
    st.markdown(
        f'<div class="section-header">Players Lost <span style="color: {COLORS["chart_negative"]}; font-weight: 500;">({len(outflows)})</span></div>',
        unsafe_allow_html=True
    )

    if outflows:
        # Sort by score
        outflows_sorted = sorted(outflows, key=lambda x: x.get("score", 0), reverse=True)

        for player in outflows_sorted:
            hs_display = f"{player['hs_rating']:.4f}" if player.get('hs_rating') else "N/A"
            games_display = f"{player['games_played']} games" if player.get('games_played', 0) > 0 else "Freshman"
            to_team = player.get("new_team", "TBD")
            player_score = player.get("score", 0)
            player_class = player.get("player_class", "Unknown")

            st.markdown(
                f"""
                <div class="player-row" style="border-left: 3px solid {COLORS['chart_negative']};">
                    <span class="outflow-badge">OUT</span>
                    <span class="player-name" style="min-width: 140px;">{player['name']}</span>
                    <span class="player-position">{player['position']}</span>
                    <span class="player-class">{player_class}</span>
                    <div style="flex: 1; display: flex; gap: 1.5rem; color: {COLORS['text_muted']}; font-size: 0.8125rem;">
                        <span>To: <strong style="color: {COLORS['text_secondary']};">{to_team}</strong></span>
                        <span>HS: {hs_display}</span>
                        <span>{games_display}</span>
                    </div>
                    <span style="color: {COLORS['chart_negative']}; font-weight: 600; margin-right: 0.5rem;">-{player_score:.1f}</span>
                    <span class="player-value" style="color: {COLORS['chart_negative']};">${player['value']:.2f}M</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expandable details
            with st.expander(f"Value breakdown for {player['name']}", expanded=False):
                breakdown = player.get("value_breakdown", {})
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown(f"**Input Data**")
                    st.markdown(f"- HS Rating: `{breakdown.get('hs_rating', 'N/A')}`")
                    st.markdown(f"- HS Normalized: `{breakdown.get('hs_normalized', 'N/A')}`")
                    st.markdown(f"- Stats Percentile: `{breakdown.get('stats_percentile', 'N/A')}`")
                    st.markdown(f"- Player Class: `{player_class}`")

                with col_b:
                    st.markdown(f"**Calculation**")
                    st.markdown(f"- HS Weight: `{breakdown.get('hs_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Stats Weight: `{breakdown.get('stats_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Position Multiplier: `{breakdown.get('position_multiplier', 1)}x`")
                    st.markdown(f"- Class Weight: `{breakdown.get('class_weight', 1)}x`")
                    st.markdown(f"- **Score: `{player_score:.1f}`**")
                    st.markdown(f"- **Value: `${breakdown.get('final_value', 0):.2f}M`**")
    else:
        st.markdown(
            f"""
            <div class="empty-state">
                <div class="empty-state-icon">📤</div>
                <p>No outflows recorded for this team.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Score comparison chart
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Score Distribution by Position</div>', unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2, gap="large")

with col_chart1:
    # Inflow by position
    if inflows:
        inflow_df = pd.DataFrame(inflows)
        pos_scores = inflow_df.groupby("position")["score"].sum().reset_index()
        pos_scores = pos_scores.sort_values("score", ascending=True)

        fig = go.Figure(go.Bar(
            x=pos_scores["score"],
            y=pos_scores["position"],
            orientation="h",
            marker_color=COLORS["accent_success"],
        ))

        fig.update_layout(
            title=dict(text="Inflow Score by Position", font=dict(size=14, color=COLORS["text_primary"])),
            plot_bgcolor=COLORS["bg_card"],
            paper_bgcolor=COLORS["bg_card"],
            font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=11),
            margin=dict(l=0, r=20, t=40, b=0),
            height=300,
            xaxis=dict(title="Score", gridcolor=COLORS["border"], titlefont=dict(size=11)),
            yaxis=dict(gridcolor=COLORS["border_light"]),
        )

        st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    # Outflow by position
    if outflows:
        outflow_df = pd.DataFrame(outflows)
        pos_scores = outflow_df.groupby("position")["score"].sum().reset_index()
        pos_scores = pos_scores.sort_values("score", ascending=True)

        fig = go.Figure(go.Bar(
            x=pos_scores["score"],
            y=pos_scores["position"],
            orientation="h",
            marker_color=COLORS["chart_negative"],
        ))

        fig.update_layout(
            title=dict(text="Outflow Score by Position", font=dict(size=14, color=COLORS["text_primary"])),
            plot_bgcolor=COLORS["bg_card"],
            paper_bgcolor=COLORS["bg_card"],
            font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=11),
            margin=dict(l=0, r=20, t=40, b=0),
            height=300,
            xaxis=dict(title="Score", gridcolor=COLORS["border"], titlefont=dict(size=11)),
            yaxis=dict(gridcolor=COLORS["border_light"]),
        )

        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        <p style="color: {COLORS['text_muted']}; font-size: 0.8125rem; margin-bottom: 0.5rem;">Want to understand how player scores are calculated?</p>
        <a href="/About" style="color: {COLORS['accent_primary']}; font-weight: 500;">View our scoring methodology →</a>
    </div>
    """,
    unsafe_allow_html=True
)
