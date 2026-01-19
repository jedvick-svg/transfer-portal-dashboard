"""
Transfer Portal Dashboard - Main Application

A modern, polished dashboard for tracking college football transfer portal activity.
Inspired by Linear, Vercel, and Stripe's dashboard aesthetic.

Version: 1.1.0
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import our modules
from src.theme import (
    get_custom_css, COLORS, render_top_nav, render_metric_card_clickable,
    render_team_card_clickable, get_team_logo
)
from src.data import get_team_data, get_summary_stats

# Page configuration
st.set_page_config(
    page_title="Transfer Portal Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Top navigation bar
st.markdown(render_top_nav(active_page="home"), unsafe_allow_html=True)

# Get data
stats = get_summary_stats()
team_df = get_team_data()

# Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">Filters</h3>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']};">Customize your view</p>
        </div>
    """, unsafe_allow_html=True)

    # Conference filter
    conferences = ["All Conferences"] + sorted(team_df["conference"].unique().tolist())
    selected_conference = st.selectbox("Conference", conferences, label_visibility="collapsed")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Sort options
    sort_options = {
        "Portal Rank": "rank",
        "Net Value (High to Low)": "net_value",
        "Total Inflow Value": "inflow_value",
        "Average Rating": "avg_rating",
        "Most Transfers": "inflows"
    }
    sort_by = st.selectbox("Sort By", list(sort_options.keys()), label_visibility="collapsed")

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

# Header
st.markdown('<h1 class="main-header">Transfer Portal Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Track college football transfer portal activity with real-time rankings and analysis</p>', unsafe_allow_html=True)

# Clickable metrics row
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(
        render_metric_card_clickable(f"{stats['total_transfers']:,}", "Total Transfers", "default", "/Database"),
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        render_metric_card_clickable(f"${stats['total_value']}M", "Total Value", "success", "/Database"),
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        render_metric_card_clickable(f"{stats['avg_rating']}", "Avg Rating", "warning", "/Database"),
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        render_metric_card_clickable(f"{stats['teams_tracked']}", "Teams Tracked", "info", "/Database"),
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Filter data
filtered_df = team_df.copy()
if selected_conference != "All Conferences":
    filtered_df = filtered_df[filtered_df["conference"] == selected_conference]

# Sort data
sort_col = sort_options[sort_by]
ascending = sort_col == "rank"
filtered_df = filtered_df.sort_values(sort_col, ascending=ascending)

# Main content - two columns with better proportions
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    st.markdown('<div class="section-header">Top 25 Team Rankings</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: {COLORS["text_muted"]}; font-size: 0.8125rem; margin-bottom: 1rem;">Click any team to view detailed transfer activity</p>', unsafe_allow_html=True)

    # Create clickable team list with logos
    for _, row in filtered_df.iterrows():
        logo_url = get_team_logo(row['team'])
        st.markdown(
            render_team_card_clickable(
                rank=row['rank'],
                team=row['team'],
                conference=row['conference'],
                value=row['inflow_value'],
                net_value=row['net_value'],
                logo_url=logo_url
            ),
            unsafe_allow_html=True
        )

with col_right:
    # Value chart with professional colors
    st.markdown('<div class="section-header">Transfer Value by Team</div>', unsafe_allow_html=True)

    chart_df = filtered_df.head(10).copy()

    fig = go.Figure()

    # Inflow bars - teal
    fig.add_trace(go.Bar(
        y=chart_df["team"],
        x=chart_df["inflow_value"],
        name="Inflow Value",
        orientation="h",
        marker_color=COLORS["chart_positive"],
    ))

    # Outflow bars - orange (softer)
    fig.add_trace(go.Bar(
        y=chart_df["team"],
        x=-chart_df["outflow_value"],
        name="Outflow Value",
        orientation="h",
        marker_color=COLORS["chart_negative"],
    ))

    fig.update_layout(
        barmode="relative",
        plot_bgcolor=COLORS["bg_card"],
        paper_bgcolor=COLORS["bg_card"],
        font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        margin=dict(l=0, r=20, t=40, b=0),
        height=420,
        xaxis=dict(
            title="Value ($M)",
            titlefont=dict(size=11, color=COLORS["text_muted"]),
            gridcolor=COLORS["border"],
            zerolinecolor=COLORS["border"],
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=COLORS["border_light"],
            autorange="reversed",
            tickfont=dict(size=11),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Conference breakdown with professional colors
    st.markdown('<div class="section-header">By Conference</div>', unsafe_allow_html=True)

    conf_df = team_df.groupby("conference").agg({
        "inflow_value": "sum",
        "outflow_value": "sum",
        "team": "count"
    }).reset_index()
    conf_df.columns = ["Conference", "Inflow Value", "Outflow Value", "Teams"]
    conf_df["Net Value"] = conf_df["Inflow Value"] - conf_df["Outflow Value"]
    conf_df = conf_df.sort_values("Net Value", ascending=False)

    # Professional color palette for pie chart
    pie_colors = [
        COLORS["chart_primary"],    # Indigo
        COLORS["chart_secondary"],  # Purple
        COLORS["chart_tertiary"],   # Sky blue
        COLORS["accent_success"],   # Teal
        COLORS["accent_warning"],   # Amber
        "#ec4899",                   # Pink
    ]

    fig2 = px.pie(
        conf_df,
        values="Inflow Value",
        names="Conference",
        color_discrete_sequence=pie_colors
    )

    fig2.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=11, color='white'),
        marker=dict(line=dict(color=COLORS["bg_card"], width=2))
    )

    fig2.update_layout(
        plot_bgcolor=COLORS["bg_card"],
        paper_bgcolor=COLORS["bg_card"],
        font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif"),
        margin=dict(l=0, r=0, t=20, b=0),
        height=280,
        showlegend=True,
        legend=dict(
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        Transfer Portal Dashboard &middot; Data sourced from 247Sports, ESPN, On3 &middot; Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
