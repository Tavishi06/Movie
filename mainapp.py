# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#                                 CINEMAVERSE
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
from datetime import datetime
from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    COLORS,
    FONTS,
    SESSION_STATE_DEFAULTS
)
from api_handlers import (
    fetch_movie_data,
    fetch_search_suggestions,
    fetch_youtube_trailer
)

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS FOR GRADIENT BACKGROUND & NEON TEXT
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
    <style>
        /* Gradient Background */
        .stApp {
            background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
            color: {COLORS['text_light']};
        }
        /* Neon Header */
        h1 {
            color: {COLORS['neon_orange']};
            text-shadow: 0 0 10px {COLORS['neon_orange']}, 0 0 20px {COLORS['neon_orange']};
        }
        .stButton>button {
            background-color: {COLORS['neon_pink']} !important;
            color: {COLORS['text_light']} !important;
            border-radius: 12px;
        }

        .stTextInput input {{
            background-color: rgba(255,255,255,0.1) !important;
            color: #fff !important;
        }}
        .stButton>button {{
            background-color: {COLORS['neon_pink']} !important;
            color: #fff !important;
            border-radius: 10px;
        }}
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────────────────
for key, value in SESSION_STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ──────────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"<h1 style='text-align:center;'>{APP_ICON} {APP_TITLE}</h1>"
    f"<p style='text-align:center;'>{APP_SUBTITLE}</p>",
    unsafe_allow_html=True
)
st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# SEARCH INPUT
# ──────────────────────────────────────────────────────────────────────────────
query = st.text_input(
    "🔍 Enter movie name",
    key="search_query",
    placeholder="Inception, Interstellar, Avatar..."
)

# ──────────────────────────────────────────────────────────────────────────────
# SEARCH SUGGESTIONS
# ──────────────────────────────────────────────────────────────────────────────
suggestions = fetch_search_suggestions(query) if query and len(query) >= 2 else []

if suggestions:
    st.markdown("### 🔮 Suggestions")
    for movie in suggestions:
        col1, col2 = st.columns([1, 6])
        with col1:
            if movie["poster"]:
                st.image(movie["poster"], width=70)
        with col2:
            if st.button(f"{movie['title']} ({movie['year']}) ⭐ {movie['rating']}", key=f"suggest_{movie['id']}"):
                st.session_state.search_query = movie["title"]
                st.session_state.should_search = True
                st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# SEARCH BUTTON
# ──────────────────────────────────────────────────────────────────────────────
if st.button("🎬 Search Movie"):
    st.session_state.should_search = True

# ──────────────────────────────────────────────────────────────────────────────
# FETCH & DISPLAY MOVIE
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.should_search and st.session_state.search_query:
    with st.spinner("🎥 Fetching movie details..."):
        movie_data, error = fetch_movie_data(st.session_state.search_query)
    st.session_state.should_search = False

    if error:
        st.error(error)
    elif movie_data:
        st.divider()

        # MOVIE TITLE
        st.markdown(f"## 🎬 {movie_data.get('Title')} ({movie_data.get('Year')})")

        col1, col2 = st.columns([1, 2])

        # POSTER
        with col1:
            poster = movie_data.get("Poster")
            if poster and poster != "N/A":
                st.image(poster, use_container_width=True)
            else:
                st.info("Poster not available")

        # DETAILS
        with col2:
            st.write("**IMDb Rating:**", movie_data.get("imdbRating"))
            st.write("**Genre:**", movie_data.get("Genre"))
            st.write("**Runtime:**", movie_data.get("Runtime"))
            st.write("**Director:**", movie_data.get("Director"))
            st.write("**Actors:**", movie_data.get("Actors"))
            st.write("**Plot:**")
            st.write(movie_data.get("Plot"))

        # TRAILER & WATCH LINK
        trailer_url = fetch_youtube_trailer(movie_data.get("Title"), movie_data.get("Year", ""))
        if trailer_url:
            st.divider()
            st.markdown("### ▶️ Official Trailer")
            st.video(trailer_url)
            st.markdown(f"[🔗 Watch on YouTube]({trailer_url})", unsafe_allow_html=True)
        else:
            search_query = f"{movie_data.get('Title')} {movie_data.get('Year', '')} full movie"
            youtube_search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            st.info("Trailer not available")
            st.markdown(f"[🔗 Search on YouTube]({youtube_search_url})", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption("🎥 CinemaVerse • Powered by OMDB, TMDB & YouTube")
