"""
Methodology Page

Explains the player valuation methodology used in the dashboard.
"""

import streamlit as st
import plotly.graph_objects as go

from src.theme import get_custom_css, COLORS, render_top_nav
from src.valuation import get_methodology_text, POSITION_MULTIPLIERS

# Page configuration
st.set_page_config(
    page_title="Methodology | Transfer Portal",
    page_icon="📊",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Top navigation bar
st.markdown(render_top_nav(active_page="about"), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">Methodology</h3>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']};">How we calculate values</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Navigation</p>
        </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py", label="Back to Rankings", icon="🏠")
    st.page_link("pages/1_Team_Details.py", label="Team Details", icon="📋")
    st.page_link("pages/3_Live_Feed.py", label="Live Feed", icon="📰")

    st.markdown("---")

    st.markdown(f"""
        <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Jump To</p>
    """, unsafe_allow_html=True)

    st.markdown("""
- [Overview](#overview)
- [Data Sources](#data-sources)
- [Weighting System](#weighting-system)
- [Position Adjustments](#position-adjustments)
- [The Formula](#the-formula)
- [Limitations](#limitations)
    """)

# Get methodology text
methodology = get_methodology_text()

# Header
st.markdown('<h1 class="main-header">Valuation Methodology</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">How we calculate transfer portal player values</p>', unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Overview section
st.markdown('<a name="overview"></a>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="methodology-card">
        <h3 style="color: {COLORS['text_primary']}; margin-top: 0; font-size: 1.125rem; font-weight: 600;">Overview</h3>
        <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin: 0;">
            {methodology['overview']}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Data Sources
st.markdown('<a name="data-sources"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)
st.markdown(methodology['data_sources'])

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        f"""
        <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-left: 3px solid {COLORS['accent_primary']}; border-radius: 10px; padding: 1.25rem; box-shadow: {COLORS['shadow_sm']};">
            <h4 style="color: {COLORS['accent_primary']}; margin-top: 0; font-size: 0.9375rem; font-weight: 600;">247Sports</h4>
            <ul style="color: {COLORS['text_secondary']}; margin: 0; padding-left: 1.25rem; line-height: 1.8; font-size: 0.875rem;">
                <li>Composite recruiting rankings</li>
                <li>Transfer portal entries</li>
                <li>Commitment tracking</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-left: 3px solid {COLORS['accent_info']}; border-radius: 10px; padding: 1.25rem; box-shadow: {COLORS['shadow_sm']};">
            <h4 style="color: {COLORS['accent_info']}; margin-top: 0; font-size: 0.9375rem; font-weight: 600;">ESPN</h4>
            <ul style="color: {COLORS['text_secondary']}; margin: 0; padding-left: 1.25rem; line-height: 1.8; font-size: 0.875rem;">
                <li>Season statistics</li>
                <li>Game-by-game performance</li>
                <li>Career totals</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Weighting System
st.markdown('<a name="weighting-system"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Experience-Based Weighting</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <p style="color: {COLORS['text_secondary']}; margin-bottom: 1rem; font-size: 0.9375rem;">
        The balance between recruiting rating and game performance shifts based on college experience.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(methodology['weighting'])

# Visual representation
weight_data = [
    {"Experience": "0-5 games", "HS Rating": 90, "Game Stats": 10},
    {"Experience": "6-20 games", "HS Rating": 50, "Game Stats": 50},
    {"Experience": "21+ games", "HS Rating": 20, "Game Stats": 80},
]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d["Experience"] for d in weight_data],
    y=[d["HS Rating"] for d in weight_data],
    name="HS Rating Weight",
    marker_color=COLORS["chart_primary"],
))

fig.add_trace(go.Bar(
    x=[d["Experience"] for d in weight_data],
    y=[d["Game Stats"] for d in weight_data],
    name="Game Stats Weight",
    marker_color=COLORS["chart_tertiary"],
))

fig.update_layout(
    barmode="stack",
    plot_bgcolor=COLORS["bg_card"],
    paper_bgcolor=COLORS["bg_card"],
    font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=12),
    margin=dict(l=0, r=0, t=20, b=0),
    height=320,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
    yaxis=dict(title="Weight (%)", gridcolor=COLORS["border"], titlefont=dict(size=11)),
    xaxis=dict(gridcolor=COLORS["border_light"]),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Position Adjustments
st.markdown('<a name="position-adjustments"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Position Value Multipliers</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <p style="color: {COLORS['text_secondary']}; margin-bottom: 1rem; font-size: 0.9375rem;">
        Not all positions are valued equally in the transfer market. These multipliers reflect market dynamics.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(methodology['position_adjustments'])

# Position multiplier chart
positions = list(POSITION_MULTIPLIERS.keys())
multipliers = list(POSITION_MULTIPLIERS.values())

# Sort by multiplier
sorted_data = sorted(zip(positions, multipliers), key=lambda x: x[1], reverse=True)
positions, multipliers = zip(*sorted_data)

fig2 = go.Figure(go.Bar(
    x=list(multipliers),
    y=list(positions),
    orientation="h",
    marker_color=[COLORS["accent_primary"] if m >= 1.0 else COLORS["accent_warning"] for m in multipliers],
    text=[f"{m:.2f}x" for m in multipliers],
    textposition="outside",
    textfont=dict(size=11),
))

fig2.update_layout(
    plot_bgcolor=COLORS["bg_card"],
    paper_bgcolor=COLORS["bg_card"],
    font=dict(color=COLORS["text_secondary"], family="Inter, -apple-system, sans-serif", size=12),
    margin=dict(l=0, r=50, t=20, b=0),
    height=400,
    xaxis=dict(title="Multiplier", gridcolor=COLORS["border"], range=[0, 1.7], titlefont=dict(size=11)),
    yaxis=dict(gridcolor=COLORS["border_light"]),
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# The Formula
st.markdown('<a name="the-formula"></a>', unsafe_allow_html=True)
st.markdown('<div class="section-header">The Formula</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="formula-box">
        <code style="color: {COLORS['accent_primary']};">Player Value</code> = Base Value × Position Multiplier<br><br>
        <code style="color: {COLORS['accent_primary']};">Base Value</code> = $0.1M + ($3.4M) × Composite Score<sup>1.5</sup><br><br>
        <code style="color: {COLORS['accent_primary']};">Composite Score</code> = (HS_Normalized × HS_Weight) + (Stats_Pct × Stats_Weight)<br><br>
        <code style="color: {COLORS['accent_primary']};">HS_Normalized</code> = (HS_Rating - 0.7000) / 0.3000
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <p style="color: {COLORS['text_secondary']}; margin-top: 1rem; font-size: 0.875rem; line-height: 1.6;">
        The exponential factor (^1.5) ensures that elite players are valued disproportionately
        higher than average players, reflecting real market dynamics.
    </p>
    """,
    unsafe_allow_html=True
)

# Example calculation
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-header">Example Calculation</div>', unsafe_allow_html=True)

with st.expander("Calculate value for a hypothetical player", expanded=True):
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        example_hs = st.slider("HS Rating (247 Composite)", 0.7500, 0.9999, 0.9200, 0.0001, format="%.4f")
        example_games = st.slider("Games Played", 0, 40, 12)
        example_stats = st.slider("Stats Percentile", 0.0, 1.0, 0.65, 0.01) if example_games > 0 else 0.0
        example_pos = st.selectbox("Position", list(POSITION_MULTIPLIERS.keys()), index=0)

    with col_b:
        from src.valuation import calculate_player_value

        result = calculate_player_value(
            hs_rating=example_hs,
            games_played=example_games,
            stats_percentile=example_stats if example_games > 0 else None,
            position=example_pos
        )

        breakdown = result["breakdown"]

        st.markdown(f"""
        <div style="background: {COLORS['bg_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 8px; padding: 1rem;">
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>HS Normalized:</strong> {breakdown['hs_normalized']:.3f}</p>
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>HS Weight:</strong> {breakdown['hs_weight']*100:.0f}%</p>
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>Stats Weight:</strong> {breakdown['stats_weight']*100:.0f}%</p>
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>Composite Score:</strong> {breakdown['composite_score']:.3f}</p>
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>Position Multiplier:</strong> {breakdown['position_multiplier']}x</p>
            <p style="margin: 0.25rem 0; font-size: 0.875rem; color: {COLORS['text_secondary']};"><strong>Raw Value:</strong> ${breakdown['raw_value']:.2f}M</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="background: {COLORS['accent_success']}15; border: 1px solid {COLORS['accent_success']}33; padding: 1rem; border-radius: 8px; margin-top: 1rem; text-align: center;">
                <span style="color: {COLORS['text_muted']}; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">Estimated Value</span>
                <div style="color: {COLORS['accent_success']}; font-size: 1.75rem; font-weight: 700; margin-top: 0.25rem;">
                    ${result['value']:.2f}M
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Limitations
st.markdown('<a name="limitations"></a>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="methodology-card" style="border-left-color: {COLORS['accent_warning']};">
        <h3 style="color: {COLORS['accent_warning']}; margin-top: 0; font-size: 1.125rem; font-weight: 600;">Limitations</h3>
        <div style="color: {COLORS['text_secondary']}; line-height: 1.7; font-size: 0.9375rem;">
            {methodology['limitations']}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        Questions about our methodology? <a href="mailto:contact@example.com" style="color: {COLORS['accent_primary']}; font-weight: 500;">Contact us</a>
    </div>
    """,
    unsafe_allow_html=True
)
