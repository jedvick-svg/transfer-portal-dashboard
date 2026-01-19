"""
NIL or Nothing - Transfer Portal Dashboard

A modern analytics dashboard for tracking college football transfer portal activity.
Teams are ranked by their composite SCORE, not dollar value.

Version: 2.0.0
"""

import streamlit as st
import plotly.graph_objects as go

from src.theme import (
    get_custom_css, COLORS, render_brand_header, render_metric_card,
    render_team_row, render_sample_data_banner, get_team_logo
)
from src.data import get_team_data, get_summary_stats, CONFERENCES

# Page configuration
st.set_page_config(
    page_title="NIL or Nothing | Transfer Portal Rankings",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Brand header
st.markdown(render_brand_header(), unsafe_allow_html=True)

# Sample data notice
st.markdown(render_sample_data_banner(), unsafe_allow_html=True)

# Get data
stats = get_summary_stats()
team_df = get_team_data()

# Navigation using Streamlit's native page links
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
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em;">Filters</p>
        </div>
    """, unsafe_allow_html=True)

    # Conference filter
    conferences = ["All Conferences"] + list(CONFERENCES.keys())
    selected_conference = st.selectbox("Conference", conferences, label_visibility="collapsed")

    st.markdown("---")

    st.markdown(
        f"""
        <div style="color: {COLORS['text_muted']}; font-size: 0.6875rem; line-height: 1.5;">
            <p style="margin-bottom: 0.25rem;">Last updated: Jan 18, 2026</p>
            <p>Data: Sample Data (Demo)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Header
st.markdown('<h1 class="main-header">Transfer Portal Rankings</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Teams ranked by composite transfer score for the 2026 offseason</p>', unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(
        render_metric_card(f"{stats['total_transfers']:,}", "Total Transfers", "default"),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        render_metric_card(f"${stats['total_nil_spent']:.1f}M", "Total NIL Spent", "success"),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        render_metric_card(f"{stats['avg_score']:.1f}", "Avg Team Score", "warning"),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        render_metric_card(f"{stats['teams_tracked']}", "Teams Tracked", "info"),
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Filter data
filtered_df = team_df.copy()
if selected_conference != "All Conferences":
    filtered_df = filtered_df[filtered_df["conference"] == selected_conference]

# Main content
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown('<div class="section-header">Team Rankings by Score</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: {COLORS["text_muted"]}; font-size: 0.8125rem; margin-bottom: 1rem;">Score = Σ(Incoming Player Scores) − Σ(Outgoing Player Scores)</p>', unsafe_allow_html=True)

    # Build the team rankings table
    table_rows = ""
    for _, row in filtered_df.iterrows():
        logo_url = get_team_logo(row['team'])

        # Format offensive/defensive player counts
        off_display = f"+{row['offensive_in']}/−{row['offensive_out']}"
        def_display = f"+{row['defensive_in']}/−{row['defensive_out']}"

        table_rows += render_team_row(
            rank=row['rank'],
            team=row['team'],
            logo_url=logo_url,
            score=row['score'],
            nil_spent=row['nil_spent'],
            off_players=off_display,
            def_players=def_display,
            conference=row['conference']
        )

    st.markdown(f"""
        <div class="team-table-container">
            <table class="team-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">Rank</th>
                        <th>Team</th>
                        <th>Score</th>
                        <th>NIL Spent</th>
                        <th>Off +/−</th>
                        <th>Def +/−</th>
                        <th>Conf</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # Score by team chart
    st.markdown('<div class="section-header">Transfer Score by Team</div>', unsafe_allow_html=True)

    chart_df = filtered_df.head(10).copy()
    chart_df = chart_df.sort_values('score', ascending=True)

    # Color bars based on positive/negative score
    colors = [COLORS["chart_positive"] if s >= 0 else COLORS["chart_negative"] for s in chart_df["score"]]

    fig = go.Figure(go.Bar(
        y=chart_df["team"],
        x=chart_df["score"],
        orientation="h",
        marker_color=colors,
        text=[f"{s:+.1f}" for s in chart_df["score"]],
        textposition="outside",
        textfont=dict(size=11),
    ))

    fig.update_layout(
        plot_bgcolor=COLORS["bg_card"],
        paper_bgcolor=COLORS["bg_card"],
        font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=12),
        margin=dict(l=0, r=60, t=20, b=0),
        height=400,
        xaxis=dict(
            title="Score",
            titlefont=dict(size=11, color=COLORS["text_muted"]),
            gridcolor=COLORS["border"],
            zerolinecolor=COLORS["border"],
        ),
        yaxis=dict(
            gridcolor=COLORS["border_light"],
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Conference breakdown
    st.markdown('<div class="section-header">Score by Conference</div>', unsafe_allow_html=True)

    conf_df = team_df.groupby("conference").agg({
        "score": "sum",
        "nil_spent": "sum",
        "team": "count"
    }).reset_index()
    conf_df.columns = ["Conference", "Total Score", "NIL Spent", "Teams"]
    conf_df = conf_df.sort_values("Total Score", ascending=False)

    # Conference score chart
    fig2 = go.Figure(go.Bar(
        x=conf_df["Conference"],
        y=conf_df["Total Score"],
        marker_color=[COLORS["chart_positive"] if s >= 0 else COLORS["chart_negative"] for s in conf_df["Total Score"]],
        text=[f"{s:+.0f}" for s in conf_df["Total Score"]],
        textposition="outside",
    ))

    fig2.update_layout(
        plot_bgcolor=COLORS["bg_card"],
        paper_bgcolor=COLORS["bg_card"],
        font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=11),
        margin=dict(l=0, r=0, t=20, b=0),
        height=250,
        xaxis=dict(tickangle=-45),
        yaxis=dict(title="Total Score", gridcolor=COLORS["border"]),
    )

    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        NIL or Nothing • Transfer Portal Analytics • Sample Data for Demonstration
    </div>
    """,
    unsafe_allow_html=True
)
