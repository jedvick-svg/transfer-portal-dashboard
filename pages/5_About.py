"""
About Page - NIL or Nothing

Comprehensive methodology explanation with position multipliers table.
"""

import streamlit as st

from src.theme import get_custom_css, COLORS, render_brand_header, render_sample_data_banner
from src.valuation import get_position_multipliers_table, get_methodology_text, CLASS_WEIGHTS

# Page configuration
st.set_page_config(
    page_title="About | NIL or Nothing",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Brand header
st.markdown(render_brand_header(), unsafe_allow_html=True)

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
        <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Jump To</p>
    """, unsafe_allow_html=True)

    st.markdown("""
- [Overview](#overview)
- [Scoring Formula](#scoring-formula)
- [Position Multipliers](#position-multipliers)
- [Class Weights](#class-weights)
- [Data Sources](#data-sources)
- [Limitations](#limitations)
    """)

# Header
st.markdown('<h1 class="main-header">About NIL or Nothing</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Understanding our transfer portal scoring methodology</p>', unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    # Overview
    st.markdown('<a name="overview"></a>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="methodology-card">
            <h3 style="color: {COLORS['text_primary']}; margin-top: 0; font-size: 1.25rem; font-weight: 600;">What is NIL or Nothing?</h3>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1rem;">
                NIL or Nothing is a comprehensive analytics platform for evaluating college football transfer portal activity.
                Unlike simple player counts or estimated NIL dollar values, we use a <strong>composite scoring system</strong> that
                weighs multiple factors to determine each team's true portal success.
            </p>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7;">
                Teams are ranked by their <strong>net score</strong>: the sum of incoming player scores minus outgoing player scores.
                This approach rewards teams that gain high-value players while penalizing significant talent losses.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Scoring Formula
    st.markdown('<a name="scoring-formula"></a>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Scoring Formula</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="methodology-card">
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1.5rem;">
                Each player's score is calculated using a weighted composite of their recruiting rating, on-field performance,
                positional value, and experience level. The team score aggregates all player movements.
            </p>

            <div class="formula-display">
                <div class="formula">
                    <span class="formula-part" style="font-size: 1.1rem; font-style: italic;"><strong>S<sub>team</sub></strong> = Σ S<sub>in</sub> − Σ S<sub>out</sub></span>
                    <span class="formula-part" style="margin-top: 1rem; font-size: 1.1rem; font-style: italic;"><strong>S<sub>player</sub></strong> = R × P × C × 100</span>
                    <span class="formula-part" style="margin-top: 1rem; font-size: 1.1rem; font-style: italic;"><strong>R</strong> = (w<sub>hs</sub> × r<sub>hs</sub>) + (w<sub>stats</sub> × r<sub>stats</sub>)</span>
                </div>
            </div>

            <h4 style="color: {COLORS['text_primary']}; margin-top: 1.5rem; font-size: 1rem;">Variable Definitions</h4>

            <table class="position-table" style="margin-top: 0.5rem;">
                <thead>
                    <tr>
                        <th>Variable</th>
                        <th>Description</th>
                        <th>Range</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-style: italic;">S<sub>team</sub></td>
                        <td>Team's net transfer portal score</td>
                        <td>Any value (+ or −)</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">S<sub>player</sub></td>
                        <td>Individual player's composite score</td>
                        <td>0 to ~170</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">R</td>
                        <td>Player's combined rating (recruiting + performance)</td>
                        <td>0 to 1</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">P</td>
                        <td>Position multiplier (QB highest, specialists lowest)</td>
                        <td>0.45 to 1.50</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">C</td>
                        <td>Class weight (Graduate highest, Freshman lowest)</td>
                        <td>0.70 to 1.15</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">r<sub>hs</sub></td>
                        <td>High school recruiting rating (normalized)</td>
                        <td>0 to 1</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">r<sub>stats</sub></td>
                        <td>On-field performance percentile</td>
                        <td>0 to 1</td>
                    </tr>
                    <tr>
                        <td style="font-style: italic;">w<sub>hs</sub>, w<sub>stats</sub></td>
                        <td>Rating weights (must sum to 1.0)</td>
                        <td>See table below</td>
                    </tr>
                </tbody>
            </table>

            <h4 style="color: {COLORS['text_primary']}; margin-top: 1.5rem; font-size: 1rem;">Experience-Based Rating Weights</h4>
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1rem;">
                As players gain college experience, we shift emphasis from recruiting rating to actual performance:
            </p>

            <table class="position-table" style="margin-top: 0.5rem;">
                <thead>
                    <tr>
                        <th>Games Played</th>
                        <th style="font-style: italic;">w<sub>hs</sub></th>
                        <th style="font-style: italic;">w<sub>stats</sub></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>0–5 games</td>
                        <td>0.90</td>
                        <td>0.10</td>
                    </tr>
                    <tr>
                        <td>6–20 games</td>
                        <td>0.50</td>
                        <td>0.50</td>
                    </tr>
                    <tr>
                        <td>21+ games</td>
                        <td>0.20</td>
                        <td>0.80</td>
                    </tr>
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Position Multipliers Table
    st.markdown('<a name="position-multipliers"></a>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Position Multipliers</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <p style="color: {COLORS['text_secondary']}; margin-bottom: 1rem; font-size: 0.9375rem;">
            Not all positions are valued equally in the transfer market. These multipliers reflect each position's
            strategic importance, scarcity of elite talent, and historical impact on team success.
        </p>
    """, unsafe_allow_html=True)

    # Build position multipliers table
    position_data = get_position_multipliers_table()

    table_rows = ""
    for pos in position_data:
        table_rows += f"""
        <tr>
            <td>{pos['position']}</td>
            <td>{pos['multiplier']:.2f}x</td>
            <td>{pos['reasoning']}</td>
        </tr>
        """

    st.markdown(f"""
        <div class="methodology-card" style="padding: 0; overflow: hidden;">
            <table class="position-table">
                <thead>
                    <tr>
                        <th>Position</th>
                        <th>Multiplier</th>
                        <th>Reasoning</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Class Weights
    st.markdown('<a name="class-weights"></a>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Class Weights</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="methodology-card">
            <p style="color: {COLORS['text_secondary']}; line-height: 1.7; margin-bottom: 1rem;">
                Player class affects their immediate impact potential. Graduate transfers and seniors can contribute
                immediately, while younger players may need development time.
            </p>

            <table class="position-table">
                <thead>
                    <tr>
                        <th>Class</th>
                        <th>Weight</th>
                        <th>Rationale</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Graduate</td><td>1.15x</td><td>Immediate eligibility, experienced leadership, proven at college level</td></tr>
                    <tr><td>Redshirt Senior</td><td>1.10x</td><td>Seasoned player with one year remaining, mature and developed</td></tr>
                    <tr><td>Senior</td><td>1.05x</td><td>Experienced player, immediate contributor with proven track record</td></tr>
                    <tr><td>Redshirt Junior</td><td>1.00x</td><td>Baseline - full experience with multiple years of eligibility</td></tr>
                    <tr><td>Junior</td><td>0.95x</td><td>Good experience level, still developing but can contribute</td></tr>
                    <tr><td>Redshirt Sophomore</td><td>0.90x</td><td>Developing player with some experience, upside potential</td></tr>
                    <tr><td>Sophomore</td><td>0.85x</td><td>Limited college experience, may need more development</td></tr>
                    <tr><td>Redshirt Freshman</td><td>0.75x</td><td>Minimal college experience, mostly evaluated on recruiting ranking</td></tr>
                    <tr><td>Freshman</td><td>0.70x</td><td>No college experience, entirely based on high school evaluation</td></tr>
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Limitations
    st.markdown('<a name="limitations"></a>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="methodology-card" style="border-left: 4px solid {COLORS['accent_warning']};">
            <h4 style="color: {COLORS['accent_warning']}; margin-top: 0; font-size: 1rem; font-weight: 600;">Limitations & Disclaimers</h4>
            <ul style="color: {COLORS['text_secondary']}; line-height: 2; padding-left: 1.25rem; margin: 0;">
                <li><strong>NIL Market Dynamics:</strong> Actual NIL deals depend on marketability, social following, and team needs—factors we don't model</li>
                <li><strong>Scheme Fit:</strong> A player's value varies significantly based on how well they fit a team's offensive or defensive scheme</li>
                <li><strong>Character/Leadership:</strong> Intangible qualities like leadership and locker room presence aren't quantifiable</li>
                <li><strong>Injury History:</strong> Player health and injury concerns are not currently factored into valuations</li>
                <li><strong>Market Timing:</strong> Portal values fluctuate based on supply/demand throughout the transfer cycle</li>
                <li><strong>Sample Data:</strong> This demo uses simulated data. Real deployment would require API integration with 247Sports, On3, or ESPN</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Data Sources
    st.markdown('<a name="data-sources"></a>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)

    data_sources = [
        {
            "name": "247Sports",
            "description": "Composite recruiting rankings",
            "color": COLORS["accent_primary"],
            "items": ["Composite player ratings", "High school rankings", "Transfer portal entries", "Commitment tracking"]
        },
        {
            "name": "ESPN",
            "description": "Performance statistics",
            "color": COLORS["accent_danger"],
            "items": ["Season statistics", "Game-by-game data", "Career totals", "Team rosters"]
        },
        {
            "name": "On3",
            "description": "NIL valuations and news",
            "color": COLORS["accent_info"],
            "items": ["NIL deal estimates", "Transfer news", "Recruiting updates", "Industry analysis"]
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
        NIL or Nothing • Transfer Portal Analytics • © 2026
    </div>
    """,
    unsafe_allow_html=True
)
