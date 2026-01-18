"""
Team Details Page

Shows detailed inflows and outflows for a selected team,
including player valuations and transfer history.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.theme import get_custom_css, COLORS, TEAM_COLORS, get_team_logo
from src.data import get_all_teams_list, get_team_details, get_team_conference

# Page configuration
st.set_page_config(
    page_title="Team Details | Transfer Portal",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Get query params for direct linking
params = st.query_params
default_team = params.get("team", "Georgia")

# Sidebar - Team selector
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">Select Team</h3>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']};">View detailed transfer activity</p>
        </div>
    """, unsafe_allow_html=True)

    teams = get_all_teams_list()
    selected_team = st.selectbox(
        "Team",
        teams,
        index=teams.index(default_team) if default_team in teams else 0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Navigation</p>
        </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py", label="Back to Rankings", icon="🏠")
    st.page_link("pages/2_Methodology.py", label="Methodology", icon="📊")
    st.page_link("pages/3_Live_Feed.py", label="Live Feed", icon="📰")

# Get team data
team_data = get_team_details(selected_team)

if not team_data:
    st.error("Team not found")
    st.stop()

info = team_data["info"]
conference = team_data["conference"]
inflows = team_data["inflows"]
outflows = team_data["outflows"]

# Get team colors and logo
team_colors = TEAM_COLORS.get(selected_team, {"primary": COLORS["accent_primary"], "secondary": COLORS["text_secondary"]})
logo_url = get_team_logo(selected_team)

# Header with team branding and logo
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 2rem;">
        <div style="
            width: 72px;
            height: 72px;
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8px;
            box-shadow: {COLORS['shadow_sm']};
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

# Summary metrics
col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

net_value = info["inflow_value"] - info["outflow_value"]

with col1:
    st.markdown(
        f"""
        <div class="metric-card success">
            <p class="metric-value">{info['inflows']}</p>
            <p class="metric-label">Players In</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {COLORS['chart_negative']};">
            <p class="metric-value">{info['outflows']}</p>
            <p class="metric-label">Players Out</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card success">
            <p class="metric-value">${info['inflow_value']:.1f}M</p>
            <p class="metric-label">Inflow Value</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {COLORS['chart_negative']};">
            <p class="metric-value">${info['outflow_value']:.1f}M</p>
            <p class="metric-label">Outflow Value</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    net_prefix = "+" if net_value >= 0 else ""
    net_color = COLORS['accent_success'] if net_value >= 0 else COLORS['accent_danger']
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color: {net_color};">
            <p class="metric-value" style="color: {net_color};">{net_prefix}${net_value:.1f}M</p>
            <p class="metric-label">Net Value</p>
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
        # Sort by value
        inflows_sorted = sorted(inflows, key=lambda x: x["value"], reverse=True)

        for player in inflows_sorted:
            hs_display = f"{player['hs_rating']:.4f}" if player['hs_rating'] else "N/A"
            games_display = f"{player['games_played']} games" if player['games_played'] > 0 else "Freshman"
            from_team = player.get("previous_team", "Unknown")

            st.markdown(
                f"""
                <div class="player-row" style="border-left: 3px solid {COLORS['accent_success']};">
                    <span class="inflow-badge">IN</span>
                    <span class="player-name" style="min-width: 140px;">{player['name']}</span>
                    <span class="player-position">{player['position']}</span>
                    <div style="flex: 1; display: flex; gap: 1.5rem; color: {COLORS['text_muted']}; font-size: 0.8125rem;">
                        <span>From: <strong style="color: {COLORS['text_secondary']};">{from_team}</strong></span>
                        <span>HS: {hs_display}</span>
                        <span>{games_display}</span>
                    </div>
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

                with col_b:
                    st.markdown(f"**Calculation**")
                    st.markdown(f"- HS Weight: `{breakdown.get('hs_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Stats Weight: `{breakdown.get('stats_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Position Multiplier: `{breakdown.get('position_multiplier', 1)}x`")
                    st.markdown(f"- **Final Value: `${breakdown.get('final_value', 0):.2f}M`**")
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
        # Sort by value
        outflows_sorted = sorted(outflows, key=lambda x: x["value"], reverse=True)

        for player in outflows_sorted:
            hs_display = f"{player['hs_rating']:.4f}" if player['hs_rating'] else "N/A"
            games_display = f"{player['games_played']} games" if player['games_played'] > 0 else "Freshman"
            to_team = player.get("new_team", "TBD")

            st.markdown(
                f"""
                <div class="player-row" style="border-left: 3px solid {COLORS['chart_negative']};">
                    <span class="outflow-badge">OUT</span>
                    <span class="player-name" style="min-width: 140px;">{player['name']}</span>
                    <span class="player-position">{player['position']}</span>
                    <div style="flex: 1; display: flex; gap: 1.5rem; color: {COLORS['text_muted']}; font-size: 0.8125rem;">
                        <span>To: <strong style="color: {COLORS['text_secondary']};">{to_team}</strong></span>
                        <span>HS: {hs_display}</span>
                        <span>{games_display}</span>
                    </div>
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

                with col_b:
                    st.markdown(f"**Calculation**")
                    st.markdown(f"- HS Weight: `{breakdown.get('hs_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Stats Weight: `{breakdown.get('stats_weight', 0)*100:.0f}%`")
                    st.markdown(f"- Position Multiplier: `{breakdown.get('position_multiplier', 1)}x`")
                    st.markdown(f"- **Final Value: `${breakdown.get('final_value', 0):.2f}M`**")
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

# Value comparison chart
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Value Distribution by Position</div>', unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2, gap="large")

with col_chart1:
    # Inflow by position
    if inflows:
        inflow_df = pd.DataFrame(inflows)
        pos_values = inflow_df.groupby("position")["value"].sum().reset_index()
        pos_values = pos_values.sort_values("value", ascending=True)

        fig = go.Figure(go.Bar(
            x=pos_values["value"],
            y=pos_values["position"],
            orientation="h",
            marker_color=COLORS["accent_success"],
        ))

        fig.update_layout(
            title=dict(text="Inflow Value by Position", font=dict(size=14, color=COLORS["text_primary"])),
            plot_bgcolor=COLORS["bg_card"],
            paper_bgcolor=COLORS["bg_card"],
            font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=11),
            margin=dict(l=0, r=20, t=40, b=0),
            height=300,
            xaxis=dict(title="Value ($M)", gridcolor=COLORS["border"], titlefont=dict(size=11)),
            yaxis=dict(gridcolor=COLORS["border_light"]),
        )

        st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    # Outflow by position
    if outflows:
        outflow_df = pd.DataFrame(outflows)
        pos_values = outflow_df.groupby("position")["value"].sum().reset_index()
        pos_values = pos_values.sort_values("value", ascending=True)

        fig = go.Figure(go.Bar(
            x=pos_values["value"],
            y=pos_values["position"],
            orientation="h",
            marker_color=COLORS["chart_negative"],
        ))

        fig.update_layout(
            title=dict(text="Outflow Value by Position", font=dict(size=14, color=COLORS["text_primary"])),
            plot_bgcolor=COLORS["bg_card"],
            paper_bgcolor=COLORS["bg_card"],
            font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=11),
            margin=dict(l=0, r=20, t=40, b=0),
            height=300,
            xaxis=dict(title="Value ($M)", gridcolor=COLORS["border"], titlefont=dict(size=11)),
            yaxis=dict(gridcolor=COLORS["border_light"]),
        )

        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        <p style="color: {COLORS['text_muted']}; font-size: 0.8125rem; margin-bottom: 0.5rem;">Want to understand how player values are calculated?</p>
        <a href="/Methodology" style="color: {COLORS['accent_primary']}; font-weight: 500;">View our valuation methodology →</a>
    </div>
    """,
    unsafe_allow_html=True
)
