"""
About Page

Information about the Transfer Portal Dashboard, data sources, and methodology.
"""

import streamlit as st

from src.theme import get_custom_css, COLORS, render_top_nav
from src.valuation import POSITION_MULTIPLIERS

# Page configuration
st.set_page_config(
    page_title="About | Transfer Portal",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Top navigation bar
st.markdown(render_top_nav(active_page="about"), unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">About Transfer Portal Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Learn about our data sources, methodology, and team</p>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    # Overview
    st.markdown(f"""
        <div class="methodology-card">
            <h3 style="color: {COLORS['text_primary']}; margin-top: 0; font-size: 1.25rem; font-weight: 600;">What is the Transfer Portal Dashboard?</h3>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1rem;">
                The Transfer Portal Dashboard is a comprehensive analytics platform for tracking college football transfer portal activity.
                We aggregate data from multiple sources to provide real-time rankings, player valuations, and transfer trends across all major programs.
            </p>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7;">
                Our goal is to provide fans, analysts, and media with accurate, up-to-date information about the rapidly evolving
                landscape of college football player movement.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Data Sources
    st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)

    data_sources = [
        {
            "name": "247Sports",
            "description": "Composite recruiting rankings and transfer portal tracking",
            "color": COLORS["accent_primary"],
            "items": ["Composite player ratings", "High school recruiting data", "Transfer portal entries", "Commitment tracking"]
        },
        {
            "name": "ESPN",
            "description": "Game statistics and performance metrics",
            "color": COLORS["accent_danger"],
            "items": ["Season statistics", "Game-by-game performance", "Career totals", "Team rosters"]
        },
        {
            "name": "On3",
            "description": "NIL valuations and transfer news",
            "color": COLORS["accent_info"],
            "items": ["NIL valuations", "Transfer rumors", "Recruiting updates", "Industry analysis"]
        }
    ]

    for source in data_sources:
        items_html = "".join([f"<li>{item}</li>" for item in source["items"]])
        st.markdown(f"""
            <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-left: 4px solid {source['color']}; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem; box-shadow: {COLORS['shadow_sm']};">
                <h4 style="color: {source['color']}; margin-top: 0; font-size: 1rem; font-weight: 600;">{source['name']}</h4>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem; margin-bottom: 0.75rem;">{source['description']}</p>
                <ul style="color: {COLORS['text_muted']}; margin: 0; padding-left: 1.25rem; line-height: 1.8; font-size: 0.8125rem;">
                    {items_html}
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Methodology Overview
    st.markdown('<div class="section-header">Valuation Methodology</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="methodology-card">
            <h4 style="color: {COLORS['text_primary']}; margin-top: 0; font-size: 1rem; font-weight: 600;">How We Calculate Player Values</h4>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1rem;">
                Our player valuation model combines recruiting data with on-field performance to estimate a player's transfer market value.
                The model uses a weighted composite score that shifts based on college experience.
            </p>

            <div class="formula-box">
                <strong>Player Value</strong> = Base Value × Position Multiplier<br><br>
                <strong>Base Value</strong> = $0.1M + ($3.4M) × Composite Score<sup>1.5</sup><br><br>
                <strong>Composite Score</strong> = (HS_Rating × HS_Weight) + (Stats_Pct × Stats_Weight)
            </div>

            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-top: 1rem;">
                <strong>Experience-Based Weighting:</strong>
            </p>
            <ul style="color: {COLORS['text_secondary']}; line-height: 1.8; padding-left: 1.25rem;">
                <li><strong>0-5 games:</strong> 90% HS rating, 10% game stats</li>
                <li><strong>6-20 games:</strong> 50% HS rating, 50% game stats</li>
                <li><strong>21+ games:</strong> 20% HS rating, 80% game stats</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Limitations
    st.markdown(f"""
        <div class="methodology-card" style="border-left: 4px solid {COLORS['accent_warning']};">
            <h4 style="color: {COLORS['accent_warning']}; margin-top: 0; font-size: 1rem; font-weight: 600;">Limitations & Disclaimers</h4>
            <ul style="color: {COLORS['text_secondary']}; line-height: 1.8; padding-left: 1.25rem; margin: 0;">
                <li>Player valuations are estimates based on available data and do not reflect actual NIL deals</li>
                <li>Transfer portal status may lag behind real-time announcements</li>
                <li>Game statistics may not capture all contributions (leadership, blocking, etc.)</li>
                <li>Market dynamics can shift rapidly based on team needs and player availability</li>
                <li>This tool is for informational purposes only and should not be used for betting or financial decisions</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Quick Stats
    st.markdown('<div class="section-header">Position Multipliers</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 1.25rem; box-shadow: {COLORS['shadow_sm']};">
            <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin-bottom: 1rem;">
                Position-specific adjustments reflect market value differences
            </p>
    """, unsafe_allow_html=True)

    sorted_positions = sorted(POSITION_MULTIPLIERS.items(), key=lambda x: x[1], reverse=True)
    for pos, mult in sorted_positions:
        bar_width = int((mult / 1.5) * 100)
        color = COLORS["accent_primary"] if mult >= 1.0 else COLORS["accent_warning"]
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="min-width: 30px; font-size: 0.75rem; font-weight: 600; color: {COLORS['text_secondary']};">{pos}</span>
                <div style="flex: 1; height: 8px; background: {COLORS['border']}; border-radius: 4px; overflow: hidden;">
                    <div style="width: {bar_width}%; height: 100%; background: {color}; border-radius: 4px;"></div>
                </div>
                <span style="min-width: 40px; font-size: 0.75rem; font-weight: 500; color: {color}; text-align: right;">{mult:.2f}x</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Contact
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Contact</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 1.25rem; box-shadow: {COLORS['shadow_sm']};">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem; line-height: 1.7; margin: 0;">
                Have questions, feedback, or data corrections?
            </p>
            <p style="margin-top: 1rem; margin-bottom: 0;">
                <a href="mailto:jedvick@stanford.edu" style="color: {COLORS['accent_primary']}; font-weight: 500;">jedvick@stanford.edu</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Built With
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Built With</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="background: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 1.25rem; box-shadow: {COLORS['shadow_sm']};">
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span style="background: {COLORS['bg_secondary']}; padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: {COLORS['text_secondary']};">Streamlit</span>
                <span style="background: {COLORS['bg_secondary']}; padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: {COLORS['text_secondary']};">Python</span>
                <span style="background: {COLORS['bg_secondary']}; padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: {COLORS['text_secondary']};">Plotly</span>
                <span style="background: {COLORS['bg_secondary']}; padding: 0.375rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: {COLORS['text_secondary']};">Pandas</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        Transfer Portal Dashboard &middot; Built with Streamlit &middot; &copy; 2026
    </div>
    """,
    unsafe_allow_html=True
)
