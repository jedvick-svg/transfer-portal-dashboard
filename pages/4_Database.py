"""
Database Page

Comprehensive database of all transfer portal movements with filtering, sorting, and search.
"""

import streamlit as st
import pandas as pd

from src.theme import get_custom_css, COLORS, render_top_nav, render_back_button
from src.data import get_team_data, get_all_teams_list, get_team_details, CONFERENCES

# Page configuration
st.set_page_config(
    page_title="Database | Transfer Portal",
    page_icon="🏈",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Top navigation bar
st.markdown(render_top_nav(active_page="database"), unsafe_allow_html=True)


@st.cache_data
def get_all_transfers():
    """Get all transfer data from all teams."""
    all_transfers = []
    teams = get_all_teams_list()

    for team in teams:
        team_data = get_team_details(team)
        if team_data:
            # Add inflows
            for player in team_data["inflows"]:
                all_transfers.append({
                    "Player": player["name"],
                    "Position": player["position"],
                    "From": player.get("previous_team", "Unknown"),
                    "To": team,
                    "Rating": player["hs_rating"],
                    "Value ($M)": player["value"],
                    "Games": player["games_played"],
                    "Date": player.get("transfer_date", "Jan 2026"),
                    "Type": "Inflow",
                    "Conference": team_data["conference"]
                })

            # Add outflows
            for player in team_data["outflows"]:
                all_transfers.append({
                    "Player": player["name"],
                    "Position": player["position"],
                    "From": team,
                    "To": player.get("new_team", "TBD"),
                    "Rating": player["hs_rating"],
                    "Value ($M)": player["value"],
                    "Games": player["games_played"],
                    "Date": player.get("transfer_date", "Jan 2026"),
                    "Type": "Outflow",
                    "Conference": team_data["conference"]
                })

    return pd.DataFrame(all_transfers)


# Header
st.markdown('<h1 class="main-header">Transfer Database</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Complete database of all transfer portal movements</p>', unsafe_allow_html=True)

# Get all transfers
with st.spinner("Loading transfer data..."):
    df = get_all_transfers()

# Sidebar filters
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">Filters</h3>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']};">Narrow down results</p>
        </div>
    """, unsafe_allow_html=True)

    # Search
    search_query = st.text_input("Search", placeholder="Player, team, or position...", label_visibility="collapsed")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Conference filter
    all_conferences = ["All Conferences"] + list(CONFERENCES.keys())
    selected_conference = st.selectbox("Conference", all_conferences)

    # Position filter
    all_positions = ["All Positions"] + sorted(df["Position"].unique().tolist())
    selected_position = st.selectbox("Position", all_positions)

    # Transfer type
    transfer_type = st.selectbox("Transfer Type", ["All", "Inflows", "Outflows"])

    st.markdown("---")

    # Rating range
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

    # Value range
    st.markdown(f'<p style="font-size: 0.75rem; font-weight: 500; color: {COLORS["text_muted"]}; margin-bottom: 0.5rem; margin-top: 1rem;">Value Range ($M)</p>', unsafe_allow_html=True)
    min_value, max_value = st.slider(
        "Value",
        min_value=0.0,
        max_value=float(df["Value ($M)"].max()) + 0.5,
        value=(0.0, float(df["Value ($M)"].max()) + 0.5),
        step=0.1,
        format="%.1f",
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Reset filters button
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

# Apply filters
filtered_df = df.copy()

if search_query:
    search_lower = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Player"].str.lower().str.contains(search_lower) |
        filtered_df["From"].str.lower().str.contains(search_lower) |
        filtered_df["To"].str.lower().str.contains(search_lower) |
        filtered_df["Position"].str.lower().str.contains(search_lower)
    ]

if selected_conference != "All Conferences":
    filtered_df = filtered_df[filtered_df["Conference"] == selected_conference]

if selected_position != "All Positions":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]

if transfer_type == "Inflows":
    filtered_df = filtered_df[filtered_df["Type"] == "Inflow"]
elif transfer_type == "Outflows":
    filtered_df = filtered_df[filtered_df["Type"] == "Outflow"]

filtered_df = filtered_df[
    (filtered_df["Rating"] >= min_rating) &
    (filtered_df["Rating"] <= max_rating) &
    (filtered_df["Value ($M)"] >= min_value) &
    (filtered_df["Value ($M)"] <= max_value)
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
    avg_rating = filtered_df["Rating"].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card warning">
            <p class="metric-value">{avg_rating:.4f}</p>
            <p class="metric-label">Avg Rating</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_value = filtered_df["Value ($M)"].mean() if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card info">
            <p class="metric-value">${avg_value:.2f}M</p>
            <p class="metric-label">Avg Value</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# Sort options
sort_col1, sort_col2 = st.columns([3, 1])
with sort_col1:
    st.markdown(f'<p style="color: {COLORS["text_secondary"]}; font-size: 0.875rem;">Showing {len(filtered_df):,} transfers</p>', unsafe_allow_html=True)

with sort_col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Value (High to Low)", "Value (Low to High)", "Rating (High to Low)", "Rating (Low to High)", "Player (A-Z)", "Date"],
        label_visibility="collapsed"
    )

# Apply sorting
if sort_by == "Value (High to Low)":
    filtered_df = filtered_df.sort_values("Value ($M)", ascending=False)
elif sort_by == "Value (Low to High)":
    filtered_df = filtered_df.sort_values("Value ($M)", ascending=True)
elif sort_by == "Rating (High to Low)":
    filtered_df = filtered_df.sort_values("Rating", ascending=False)
elif sort_by == "Rating (Low to High)":
    filtered_df = filtered_df.sort_values("Rating", ascending=True)
elif sort_by == "Player (A-Z)":
    filtered_df = filtered_df.sort_values("Player", ascending=True)

# Pagination
items_per_page = 25
total_pages = max(1, (len(filtered_df) - 1) // items_per_page + 1)

if "db_page" not in st.session_state:
    st.session_state.db_page = 1

# Ensure page is valid
if st.session_state.db_page > total_pages:
    st.session_state.db_page = 1

start_idx = (st.session_state.db_page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_df = filtered_df.iloc[start_idx:end_idx]

# Display table
if len(page_df) > 0:
    # Build HTML table
    table_rows = ""
    for _, row in page_df.iterrows():
        type_badge = f'<span class="inflow-badge">IN</span>' if row["Type"] == "Inflow" else f'<span class="outflow-badge">OUT</span>'
        value_color = COLORS["accent_success"] if row["Type"] == "Inflow" else COLORS["chart_negative"]

        table_rows += f"""
        <tr>
            <td>{type_badge}</td>
            <td><strong>{row["Player"]}</strong></td>
            <td><span class="player-position">{row["Position"]}</span></td>
            <td>{row["From"]}</td>
            <td>{row["To"]}</td>
            <td>{row["Rating"]:.4f}</td>
            <td style="color: {value_color}; font-weight: 600;">${row["Value ($M)"]:.2f}M</td>
            <td>{row["Games"]}</td>
            <td style="color: {COLORS['text_muted']};">{row["Date"]}</td>
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
                        <th>From</th>
                        <th>To</th>
                        <th>Rating</th>
                        <th>Value</th>
                        <th>Games</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

    # Pagination controls
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
        Transfer Portal Database &middot; Data sourced from 247Sports, ESPN, On3
    </div>
    """,
    unsafe_allow_html=True
)
