"""
Database Page - NIL or Nothing

Comprehensive database of all transfer portal movements with filtering, sorting, and search.
"""

import streamlit as st
import pandas as pd

from src.theme import get_custom_css, COLORS, render_brand_header, render_sample_data_banner
from src.data import get_all_transfers, get_all_teams_list, CONFERENCES, ALL_POSITIONS

# Page configuration
st.set_page_config(
    page_title="Database | NIL or Nothing",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Brand header
st.markdown(render_brand_header(), unsafe_allow_html=True)


@st.cache_data
def load_transfer_data():
    """Load and cache transfer data."""
    return get_all_transfers()


# Get all transfers
with st.spinner("Loading transfer data..."):
    df = load_transfer_data()

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
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em;">Filters</p>
        </div>
    """, unsafe_allow_html=True)

    # Search
    search_query = st.text_input("Search", placeholder="Player, team, or position...", label_visibility="collapsed")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Conference filter
    all_conferences = ["All Conferences"] + list(CONFERENCES.keys())
    selected_conference = st.selectbox("Conference", all_conferences)

    # Position filter
    all_positions = ["All Positions"] + sorted(list(set(ALL_POSITIONS)))
    selected_position = st.selectbox("Position", all_positions)

    # Team filter
    all_teams = ["All Teams"] + sorted(get_all_teams_list())
    selected_team = st.selectbox("Team (From/To)", all_teams)

    # Transfer type
    transfer_type = st.selectbox("Transfer Type", ["All", "Incoming", "Outgoing"])

    st.markdown("---")

    # Rating range (convert to star ratings)
    st.markdown(f'<p style="font-size: 0.75rem; font-weight: 500; color: {COLORS["text_muted"]}; margin-bottom: 0.5rem;">Rating Range</p>', unsafe_allow_html=True)
    min_rating, max_rating = st.slider(
        "Rating",
        min_value=0.80,
        max_value=1.00,
        value=(0.80, 1.00),
        step=0.01,
        format="%.2f",
        label_visibility="collapsed"
    )

    # Class filter
    st.markdown(f'<p style="font-size: 0.75rem; font-weight: 500; color: {COLORS["text_muted"]}; margin-bottom: 0.5rem; margin-top: 1rem;">Player Class</p>', unsafe_allow_html=True)
    class_options = ["All Classes", "Freshman", "Redshirt Freshman", "Sophomore", "Redshirt Sophomore",
                    "Junior", "Redshirt Junior", "Senior", "Redshirt Senior", "Graduate"]
    selected_class = st.selectbox("Class", class_options, label_visibility="collapsed")

    st.markdown("---")

    # Reset filters button
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

# Header
st.markdown('<h1 class="main-header">Transfer Database</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Complete database of all transfer portal movements</p>', unsafe_allow_html=True)

# Sample data notice
st.markdown(render_sample_data_banner(), unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()

if search_query:
    search_lower = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Player"].str.lower().str.contains(search_lower, na=False) |
        filtered_df["From"].str.lower().str.contains(search_lower, na=False) |
        filtered_df["To"].str.lower().str.contains(search_lower, na=False) |
        filtered_df["Position"].str.lower().str.contains(search_lower, na=False)
    ]

if selected_conference != "All Conferences":
    filtered_df = filtered_df[filtered_df["Conference"] == selected_conference]

if selected_position != "All Positions":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]

if selected_team != "All Teams":
    filtered_df = filtered_df[
        (filtered_df["From"] == selected_team) |
        (filtered_df["To"] == selected_team)
    ]

if transfer_type == "Incoming":
    filtered_df = filtered_df[filtered_df["Type"] == "Inflow"]
elif transfer_type == "Outgoing":
    filtered_df = filtered_df[filtered_df["Type"] == "Outflow"]

if selected_class != "All Classes":
    filtered_df = filtered_df[filtered_df["Class"] == selected_class]

filtered_df = filtered_df[
    (filtered_df["Rating"] >= min_rating) &
    (filtered_df["Rating"] <= max_rating)
]

# Stats summary
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{len(filtered_df):,}</p>
            <p class="metric-label">Total Transfers</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    total_value = filtered_df["Value ($M)"].sum()
    st.markdown(f"""
        <div class="metric-card success">
            <p class="metric-value">${total_value:.1f}M</p>
            <p class="metric-label">Total Value</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_score = filtered_df["Score"].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card warning">
            <p class="metric-value">{avg_score:.1f}</p>
            <p class="metric-label">Avg Score</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_rating = filtered_df["Rating"].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card info">
            <p class="metric-value">{avg_rating:.4f}</p>
            <p class="metric-label">Avg Rating</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Row display and sort controls
control_col1, control_col2, control_col3 = st.columns([2, 1, 1])

with control_col1:
    # Row display options
    rows_per_page_options = {"Show 25": 25, "Show 100": 100, "Show All": len(filtered_df) if len(filtered_df) > 0 else 1}
    rows_selection = st.selectbox("Rows per page", list(rows_per_page_options.keys()), index=1, label_visibility="collapsed")
    items_per_page = rows_per_page_options[rows_selection]

with control_col2:
    # Sort column selection
    sort_columns = {
        "Score (High to Low)": ("Score", False),
        "Score (Low to High)": ("Score", True),
        "Value (High to Low)": ("Value ($M)", False),
        "Value (Low to High)": ("Value ($M)", True),
        "Rating (High to Low)": ("Rating", False),
        "Rating (Low to High)": ("Rating", True),
        "Player (A-Z)": ("Player", True),
        "Player (Z-A)": ("Player", False),
        "Date Transferred": ("Date Transferred", False),
    }
    sort_by = st.selectbox("Sort by", list(sort_columns.keys()), label_visibility="collapsed")

with control_col3:
    st.markdown(f'<p style="color: {COLORS["text_secondary"]}; font-size: 0.875rem; padding: 0.5rem 0;">Showing {len(filtered_df):,} transfers</p>', unsafe_allow_html=True)

# Apply sorting
sort_col, ascending = sort_columns[sort_by]
filtered_df = filtered_df.sort_values(sort_col, ascending=ascending)

# Pagination
total_records = len(filtered_df)
total_pages = max(1, (total_records - 1) // items_per_page + 1)

if "db_page" not in st.session_state:
    st.session_state.db_page = 1

# Ensure page is valid
if st.session_state.db_page > total_pages:
    st.session_state.db_page = 1

start_idx = (st.session_state.db_page - 1) * items_per_page
end_idx = min(start_idx + items_per_page, total_records)
page_df = filtered_df.iloc[start_idx:end_idx]

# Display showing info
st.markdown(f'<p style="color: {COLORS["text_muted"]}; font-size: 0.8125rem; margin-bottom: 0.5rem;">Showing {start_idx + 1}-{end_idx} of {total_records:,} transfers</p>', unsafe_allow_html=True)

# Display table
if len(page_df) > 0:
    # Build HTML table with sortable headers
    table_rows = ""
    for _, row in page_df.iterrows():
        type_badge = f'<span class="inflow-badge">IN</span>' if row["Type"] == "Inflow" else f'<span class="outflow-badge">OUT</span>'
        value_color = COLORS["accent_success"] if row["Type"] == "Inflow" else COLORS["chart_negative"]
        score_color = COLORS["accent_success"] if row["Score"] > 0 else COLORS["text_secondary"]

        table_rows += f"""
        <tr>
            <td>{type_badge}</td>
            <td><strong>{row["Player"]}</strong></td>
            <td><span class="player-position">{row["Position"]}</span></td>
            <td><span class="player-class">{row["Class"]}</span></td>
            <td>{row["From"]}</td>
            <td>{row["To"]}</td>
            <td>{row["Rating"]:.4f}</td>
            <td style="color: {score_color}; font-weight: 600;">{row["Score"]:.1f}</td>
            <td style="color: {value_color}; font-weight: 600;">${row["Value ($M)"]:.2f}M</td>
            <td>{row["Games"]}</td>
            <td style="color: {COLORS['text_muted']};">{row["Date Transferred"]}</td>
        </tr>
        """

    st.markdown(f"""
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Player</th>
                        <th>Pos</th>
                        <th>Class</th>
                        <th>From</th>
                        <th>To</th>
                        <th>Rating</th>
                        <th>Score</th>
                        <th>Value</th>
                        <th>Games</th>
                        <th>Date Transferred</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Pagination controls
    if total_pages > 1:
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        pag_col1, pag_col2, pag_col3, pag_col4, pag_col5 = st.columns([1, 1, 2, 1, 1])

        with pag_col1:
            if st.button("← First", disabled=st.session_state.db_page == 1, use_container_width=True):
                st.session_state.db_page = 1
                st.rerun()

        with pag_col2:
            if st.button("‹ Prev", disabled=st.session_state.db_page == 1, use_container_width=True):
                st.session_state.db_page -= 1
                st.rerun()

        with pag_col3:
            st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem; color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                    Page {st.session_state.db_page} of {total_pages}
                </div>
            """, unsafe_allow_html=True)

        with pag_col4:
            if st.button("Next ›", disabled=st.session_state.db_page == total_pages, use_container_width=True):
                st.session_state.db_page += 1
                st.rerun()

        with pag_col5:
            if st.button("Last →", disabled=st.session_state.db_page == total_pages, use_container_width=True):
                st.session_state.db_page = total_pages
                st.rerun()

else:
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">🔍</div>
            <p style="font-size: 1rem; color: {COLORS['text_secondary']}; margin-bottom: 0.25rem;">No transfers found</p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.875rem;">Try adjusting your filters</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        NIL or Nothing • Transfer Portal Database • Sample Data for Demonstration
    </div>
    """,
    unsafe_allow_html=True
)
