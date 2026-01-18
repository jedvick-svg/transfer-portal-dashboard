"""
Live Feed Page

Real-time news feed for transfer portal updates from various sources.
"""

import streamlit as st

from src.theme import get_custom_css, COLORS
from src.news_feed import get_latest_news, get_news_categories, SOURCE_COLORS

# Page configuration
st.set_page_config(
    page_title="Live Feed | Transfer Portal",
    page_icon="📰",
    layout="wide"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Additional CSS for news feed
st.markdown(
    f"""
    <style>
        .news-card {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            transition: all 150ms ease;
            box-shadow: {COLORS['shadow_sm']};
        }}

        .news-card:hover {{
            border-color: {COLORS['accent_info']};
            box-shadow: {COLORS['shadow_md']};
        }}

        .news-source-badge {{
            display: inline-block;
            padding: 0.25rem 0.625rem;
            border-radius: 9999px;
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .news-headline {{
            font-size: 1rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 0.75rem 0 0.5rem 0;
            line-height: 1.4;
        }}

        .news-summary {{
            color: {COLORS['text_secondary']};
            font-size: 0.875rem;
            line-height: 1.6;
            margin-bottom: 0.75rem;
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: {COLORS['text_muted']};
            font-size: 0.75rem;
        }}

        .live-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: {COLORS['accent_success']};
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        .live-dot {{
            width: 8px;
            height: 8px;
            background: {COLORS['accent_success']};
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h3 style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 0.25rem;">Live Feed</h3>
            <p style="font-size: 0.75rem; color: {COLORS['text_muted']};">Latest transfer news</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Navigation</p>
        </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py", label="Back to Rankings", icon="🏠")
    st.page_link("pages/1_Team_Details.py", label="Team Details", icon="📋")
    st.page_link("pages/2_Methodology.py", label="Methodology", icon="📊")

    st.markdown("---")

    st.markdown(f"""
        <p style="font-size: 0.75rem; font-weight: 600; color: {COLORS['text_muted']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Sources</p>
    """, unsafe_allow_html=True)

    for source, color in SOURCE_COLORS.items():
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <div style="width: 10px; height: 10px; background: {color}; border-radius: 3px;"></div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.8125rem;">{source}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Auto-refresh toggle
    auto_refresh = st.toggle("Auto-refresh", value=False)
    if auto_refresh:
        st.markdown(
            f"""
            <p style="color: {COLORS['text_muted']}; font-size: 0.6875rem; margin-top: 0.25rem;">
                Refreshing every 60 seconds
            </p>
            """,
            unsafe_allow_html=True
        )

# Header
col_header, col_live = st.columns([4, 1])

with col_header:
    st.markdown('<h1 class="main-header">Live Transfer Portal Feed</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Latest news, rumors, and commitments from across college football</p>', unsafe_allow_html=True)

with col_live:
    st.markdown(
        """
        <div style="text-align: right; padding-top: 1rem;">
            <span class="live-indicator">
                <span class="live-dot"></span>
                LIVE
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

# Category filters
categories = get_news_categories()

# Use session state for category selection
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "all"

# Category pills
cols = st.columns(len(categories))
for i, cat in enumerate(categories):
    with cols[i]:
        is_active = st.session_state.selected_category == cat["id"]
        if st.button(
            f"{cat['label']} ({cat['count']})",
            key=f"cat_{cat['id']}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.selected_category = cat["id"]
            st.rerun()

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Search
search_col, filter_col = st.columns([3, 1], gap="medium")
with search_col:
    search_query = st.text_input(
        "Search news",
        placeholder="Search for teams, players, or topics...",
        label_visibility="collapsed"
    )

with filter_col:
    time_filter = st.selectbox(
        "Time",
        ["All Time", "Last Hour", "Today", "This Week"],
        label_visibility="collapsed"
    )

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

# Get news based on selected category
news_items = get_latest_news(count=15, category=st.session_state.selected_category)

# Filter by search if provided
if search_query:
    search_lower = search_query.lower()
    news_items = [
        item for item in news_items
        if search_lower in item["title"].lower() or search_lower in item["summary"].lower()
    ]

# Display news feed
if news_items:
    for item in news_items:
        source_color = item.get("source_color", COLORS["accent_info"])

        # Category badge color
        cat_colors = {
            "commitment": COLORS["accent_success"],
            "entry": COLORS["accent_warning"],
            "rumor": COLORS["accent_info"],
            "analysis": COLORS["accent_secondary"],
        }
        cat_color = cat_colors.get(item["category"], COLORS["text_muted"])

        st.markdown(
            f"""
            <div class="news-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span class="news-source-badge" style="background: {source_color}15; color: {source_color};">
                        {item['source']}
                    </span>
                    <span style="color: {COLORS['text_muted']}; font-size: 0.75rem;">
                        {item['time_ago']}
                    </span>
                </div>
                <h3 class="news-headline">{item['title']}</h3>
                <p class="news-summary">{item['summary']}</p>
                <div class="news-meta">
                    <span style="background: {cat_color}15; color: {cat_color}; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.6875rem; text-transform: uppercase; font-weight: 500;">
                        {item['category']}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-icon">📰</div>
            <p style="font-size: 1rem; color: {COLORS['text_secondary']}; margin-bottom: 0.25rem;">No news found</p>
            <p style="color: {COLORS['text_muted']}; font-size: 0.875rem;">Try adjusting your search or filters</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load more button
if news_items:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col_load = st.columns([1, 2, 1])[1]
    with col_load:
        if st.button("Load More", use_container_width=True):
            st.info("In production, this would load additional news items.")

# Footer
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.75rem; padding: 1.5rem 0; border-top: 1px solid {COLORS['border']};">
        News aggregated from ESPN, 247Sports, On3, Rivals, and social media &middot; Updates refresh automatically
    </div>
    """,
    unsafe_allow_html=True
)
