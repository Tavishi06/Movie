# ═══════════════════════════════════════════════════════════════════════════════
#                           CINEMAVERSE v2.1 - ENHANCED SEARCH EDITION
#                        Explore the Universe of Movies
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import requests
from PIL import Image
import numpy as np
import io
from typing import Tuple, Dict, Optional, List
from datetime import datetime
import time

# ═══════════════════════════════════════════════════════════════════════════════
#                              CONFIGURATION SECTION
# ═══════════════════════════════════════════════════════════════════════════════

API_KEYS = {
    "omdb": "b501ccee",
    "tmdb": "5ad127b6be5b77aa124a8c1743dd33e7",
    "youtube": "AIzaSyBwB_Ls-jh-9KmVtirmUueQAFC8OG5uPzM",
    "watchmode": "8e4svmLGGt4J6vyCqMMrcAu4OoIWg3ETaz4Mzsxq"
}

# Maximum items to store in history
MAX_HISTORY = 10
MAX_FAVORITES = 20

# ═══════════════════════════════════════════════════════════════════════════════
#                              PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="CinemaVerse | Explore the Universe of Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
#                           SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state():
    """Initialize all session state variables."""
    
    defaults = {
        'search_query': '',
        'search_history': [],
        'favorites': [],
        'current_movie': None,
        'should_search': False,
        'selected_genre': 'All',
        'year_range': (1900, datetime.now().year),
        'search_suggestions': [],
        'show_suggestions': False,
        'last_search_time': 0,
        'sidebar_section': 'search'  # 'search', 'history', 'favorites', 'trending'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# ═══════════════════════════════════════════════════════════════════════════════
#                           FUTURISTIC CSS STYLES
# ═══════════════════════════════════════════════════════════════════════════════

def apply_futuristic_theme():
    """Applies the futuristic cyberpunk-inspired theme."""
    
    futuristic_css = """
    <style>
        /* ═══════ FONTS ═══════ */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
        /* ═══════ ROOT VARIABLES ═══════ */
        :root {
            --neon-blue: #00f5ff;
            --neon-purple: #bf00ff;
            --neon-pink: #ff006e;
            --neon-green: #00ff88;
            --neon-orange: #ff9500;
            --dark-bg: #0a0a0f;
            --card-bg: rgba(15, 15, 25, 0.9);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --border-glow: rgba(0, 245, 255, 0.3);
        }
        
        /* ═══════ MAIN BACKGROUND ═══════ */
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
            background-attachment: fixed;
        }
        
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }
        
        /* ═══════ TYPOGRAPHY ═══════ */
        html, body, [class*="css"] {
            font-family: 'Rajdhani', sans-serif;
            color: #e0e0e0;
        }
        
        h1, h2, h3, .title-text {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* ═══════ ENHANCED SIDEBAR ═══════ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 10, 20, 0.98) 0%, rgba(26, 10, 46, 0.98) 100%);
            border-right: 1px solid var(--border-glow);
            box-shadow: 5px 0 30px rgba(0, 245, 255, 0.1);
        }
        
        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple), var(--neon-pink));
        }
        
        /* ═══════ ENHANCED INPUT FIELDS ═══════ */
        .stTextInput input {
            background: rgba(10, 10, 20, 0.95) !important;
            border: 2px solid rgba(0, 245, 255, 0.5) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 16px !important;
            padding: 14px 18px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: var(--neon-blue) !important;
            box-shadow: none !important;
            background: rgba(10, 10, 20, 0.98) !important;
        }
        
        .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        
        /* ═══════ ENHANCED BUTTONS ═══════ */
        .stButton > button {
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple)) !important;
            border: none !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            padding: 12px 20px !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            background: linear-gradient(135deg, var(--neon-purple), var(--neon-blue)) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
        }
        
        /* Movie view button style */
        .movie-view-btn button {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(191, 0, 255, 0.2)) !important;
            border: 1px solid var(--border-glow) !important;
            color: #fff !important;
            padding: 10px 16px !important;
            font-size: 12px !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .movie-view-btn button:hover {
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple)) !important;
            border-color: var(--neon-blue) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Secondary button style */
        .secondary-btn button {
            background: transparent !important;
            border: 1px solid var(--border-glow) !important;
            box-shadow: none !important;
        }
        
        .secondary-btn button:hover {
            background: rgba(0, 245, 255, 0.1) !important;
            box-shadow: 0 5px 20px rgba(0, 245, 255, 0.2) !important;
        }
        
        /* ═══════ SEARCH SUGGESTION BOX ═══════ */
        .suggestion-box {
            background: rgba(15, 15, 30, 0.98);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            margin-top: 5px;
            max-height: 300px;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }
        
        .suggestion-item {
            padding: 12px 16px;
            cursor: pointer;
            border-bottom: 1px solid rgba(0, 245, 255, 0.1);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .suggestion-item:hover {
            background: rgba(0, 245, 255, 0.1);
        }
        
        .suggestion-item:last-child {
            border-bottom: none;
        }
        
        .suggestion-poster {
            width: 40px;
            height: 60px;
            border-radius: 6px;
            object-fit: cover;
        }
        
        .suggestion-info {
            flex: 1;
        }
        
        .suggestion-title {
            color: #fff;
            font-weight: 600;
            font-size: 14px;
        }
        
        .suggestion-year {
            color: var(--neon-blue);
            font-size: 12px;
        }
        
        /* ═══════ SIDEBAR SECTIONS ═══════ */
        .sidebar-section-header {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 0;
            color: var(--neon-blue);
            font-family: 'Orbitron', sans-serif;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(0, 245, 255, 0.2);
            margin-bottom: 10px;
        }
        
        .sidebar-nav {
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .nav-btn {
            padding: 8px 12px;
            border-radius: 8px;
            background: rgba(0, 245, 255, 0.05);
            border: 1px solid rgba(0, 245, 255, 0.2);
            color: #888;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .nav-btn:hover, .nav-btn.active {
            background: rgba(0, 245, 255, 0.15);
            border-color: var(--neon-blue);
            color: var(--neon-blue);
        }
        
        /* ═══════ HISTORY/FAVORITES ITEMS ═══════ */
        .history-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            margin: 5px 0;
            background: rgba(0, 245, 255, 0.03);
            border: 1px solid rgba(0, 245, 255, 0.1);
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .history-item:hover {
            background: rgba(0, 245, 255, 0.1);
            border-color: var(--neon-blue);
            transform: translateX(5px);
        }
        
        .history-title {
            color: #fff;
            font-size: 14px;
            flex: 1;
        }
        
        .history-meta {
            color: #666;
            font-size: 11px;
        }
        
        .history-remove {
            color: #ff006e;
            opacity: 0;
            transition: opacity 0.2s;
            cursor: pointer;
            padding: 5px;
        }
        
        .history-item:hover .history-remove {
            opacity: 1;
        }
        
        /* ═══════ FILTER SECTION ═══════ */
        .filter-chip {
            display: inline-block;
            padding: 6px 14px;
            margin: 3px;
            border-radius: 20px;
            background: rgba(0, 245, 255, 0.05);
            border: 1px solid rgba(0, 245, 255, 0.2);
            color: #888;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .filter-chip:hover, .filter-chip.active {
            background: rgba(0, 245, 255, 0.15);
            border-color: var(--neon-blue);
            color: var(--neon-blue);
        }
        
        /* ═══════ TRENDING CARD ═══════ */
        .trending-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px;
            margin: 8px 0;
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.05), rgba(191, 0, 255, 0.05));
            border: 1px solid rgba(0, 245, 255, 0.15);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .trending-card:hover {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.12), rgba(191, 0, 255, 0.12));
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0, 245, 255, 0.15);
        }
        
        .trending-rank {
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--neon-purple);
            width: 30px;
            text-align: center;
        }
        
        .trending-poster {
            width: 45px;
            height: 67px;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid rgba(0, 245, 255, 0.3);
        }
        
        .trending-info {
            flex: 1;
        }
        
        .trending-title {
            color: #fff;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        }
        
        .trending-meta {
            color: #888;
            font-size: 11px;
        }
        
        .trending-rating {
            color: var(--neon-green);
            font-family: 'Orbitron', sans-serif;
            font-size: 12px;
        }
        
        /* ═══════ TABS ═══════ */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--glass-bg);
            border-radius: 15px;
            padding: 5px;
            gap: 5px;
            border: 1px solid var(--border-glow);
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            color: #888;
            font-family: 'Orbitron', sans-serif;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(191, 0, 255, 0.2)) !important;
            color: var(--neon-blue) !important;
        }
        
        /* ═══════ STATS BAR ═══════ */
        .stats-bar {
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: rgba(0, 245, 255, 0.03);
            border-radius: 12px;
            border: 1px solid rgba(0, 245, 255, 0.1);
            margin: 15px 0;
        }
        
        .stat-mini {
            text-align: center;
        }
        
        .stat-mini-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            color: var(--neon-blue);
        }
        
        .stat-mini-label {
            font-size: 10px;
            color: #666;
            text-transform: uppercase;
        }
        
        /* ═══════ SELECT BOX ═══════ */
        .stSelectbox > div > div {
            background: rgba(0, 245, 255, 0.05) !important;
            border: 1px solid var(--border-glow) !important;
            border-radius: 10px !important;
        }
        
        /* ═══════ SLIDER ═══════ */
        .stSlider > div > div > div {
            background: var(--neon-blue) !important;
        }
        
        /* ═══════ ANIMATIONS ═══════ */
        @keyframes borderGlow {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 245, 255, 0.3); }
            50% { box-shadow: 0 0 40px rgba(0, 245, 255, 0.6); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* ═══════ CUSTOM CLASSES ═══════ */
        .cyber-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .cyber-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent);
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(191, 0, 255, 0.1));
            border: 1px solid rgba(0, 245, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 245, 255, 0.2);
        }
        
        .stat-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: var(--neon-blue);
        }
        
        .stat-label {
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 5px;
        }
        
        .streaming-badge {
            display: inline-block;
            padding: 12px 24px;
            margin: 6px;
            border-radius: 25px;
            background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(191, 0, 255, 0.1));
            border: 1px solid var(--border-glow);
            color: #fff;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .streaming-badge:hover {
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 245, 255, 0.4);
        }
        
        .movie-poster {
            border-radius: 20px;
            border: 2px solid var(--border-glow);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        
        .welcome-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 48px;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple), var(--neon-pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent);
            margin: 15px 0;
        }
        
        .info-label {
            color: #888;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .info-value {
            color: #fff;
            font-size: 16px;
            font-weight: 500;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* ═══════ KEYBOARD SHORTCUT HINT ═══════ */
        .keyboard-hint {
            font-size: 10px;
            color: #555;
            text-align: center;
            margin-top: 5px;
        }
        
        .kbd {
            display: inline-block;
            padding: 2px 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-family: monospace;
            font-size: 10px;
        }
        
    </style>
    """
    
    st.markdown(futuristic_css, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#                              API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def fetch_movie_data(movie_title):
    """Fetches movie information from OMDB and TMDB APIs."""
    
    try:
        omdb_url = f"http://www.omdbapi.com/?t={movie_title}&plot=full&apikey={API_KEYS['omdb']}"
        omdb_response = requests.get(omdb_url, timeout=15)
        omdb_data = omdb_response.json()
        
        if omdb_data.get('Response') == 'False':
            return None, f"❌ Movie '{movie_title}' not found. Try checking the spelling!"
        
        movie_data = omdb_data
        imdb_id = movie_data.get('imdbID')
        
        if imdb_id and API_KEYS['tmdb']:
            tmdb_find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={API_KEYS['tmdb']}&external_source=imdb_id"
            tmdb_response = requests.get(tmdb_find_url, timeout=15)
            tmdb_data = tmdb_response.json()
            
            if tmdb_data.get('movie_results'):
                tmdb_id = tmdb_data['movie_results'][0]['id']
                tmdb_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEYS['tmdb']}"
                tmdb_details = requests.get(tmdb_details_url, timeout=15).json()
                movie_data = {**tmdb_details, **movie_data}
                movie_data['tmdb_id'] = tmdb_id
        
        return movie_data, None
        
    except requests.exceptions.Timeout:
        return None, "⏱️ Connection timed out. Please try again!"
    except requests.exceptions.RequestException as error:
        return None, f"🌐 Network error: {error}"


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_search_suggestions(query):
    """
    Fetches search suggestions as user types.
    Uses TMDB search API for real-time suggestions.
    """
    
    if not query or len(query) < 2:
        return []
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEYS['tmdb']}&query={query}&page=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        suggestions = []
        for movie in data.get('results', [])[:8]:  # Limit to 8 suggestions
            poster_path = movie.get('poster_path')
            suggestions.append({
                'id': movie['id'],
                'title': movie['title'],
                'year': movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A',
                'poster': f"https://image.tmdb.org/t/p/w92{poster_path}" if poster_path else None,
                'rating': movie.get('vote_average', 0)
            })
        
        return suggestions
    except:
        return []


@st.cache_data(ttl=3600)
def fetch_trending_movies():
    """Fetches trending movies from TMDB."""
    
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEYS['tmdb']}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        trending = []
        for movie in data.get('results', [])[:10]:
            poster_path = movie.get('poster_path')
            trending.append({
                'id': movie['id'],
                'title': movie['title'],
                'year': movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A',
                'poster': f"https://image.tmdb.org/t/p/w92{poster_path}" if poster_path else None,
                'rating': round(movie.get('vote_average', 0), 1)
            })
        
        return trending
    except:
        return []


@st.cache_data(ttl=3600)
def fetch_movies_by_genre(genre_id):
    """Fetches movies by genre from TMDB."""
    
    try:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEYS['tmdb']}&with_genres={genre_id}&sort_by=popularity.desc"
        response = requests.get(url, timeout=10)
        return response.json().get('results', [])[:10]
    except:
        return []


@st.cache_data(ttl=3600)
def fetch_recommendations(tmdb_id):
    """Gets similar movie recommendations from TMDB."""
    
    if not tmdb_id:
        return []
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/recommendations?api_key={API_KEYS['tmdb']}"
        response = requests.get(url, timeout=10)
        return response.json().get('results', [])
    except:
        return []


@st.cache_data(ttl=86400)
def fetch_streaming_info(imdb_id):
    """Gets streaming availability information."""
    
    if not imdb_id:
        return []
    
    try:
        url = f"https://api.watchmode.com/v1/title/{imdb_id}/details/?apiKey={API_KEYS['watchmode']}&append_to_response=sources"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        sources = data.get('sources', [])
        unique_sources = {}
        
        for source in sources:
            if source.get('type') == 'sub':
                source_id = source['source_id']
                if source_id not in unique_sources:
                    unique_sources[source_id] = {
                        'name': source['name'],
                        'url': source['web_url']
                    }
        
        return list(unique_sources.values())
    except:
        return []


@st.cache_data
def fetch_youtube_trailer(title, year):
    """Searches YouTube for the official movie trailer."""
    
    try:
        try:
            from googleapiclient.discovery import build
        except ImportError:
            return None
        
        youtube = build('youtube', 'v3', developerKey=API_KEYS['youtube'])
        search_query = f"{title} {year} Official Trailer"
        
        search_response = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            maxResults=1
        ).execute()
        
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            return f"https://youtube.com/watch?v={video_id}"
        return None
    except:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
#                              HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def add_to_history(movie_title, movie_data):
    """Adds a movie to search history."""
    
    history_item = {
        'title': movie_title,
        'year': movie_data.get('Year', 'N/A'),
        'poster': movie_data.get('Poster', ''),
        'timestamp': datetime.now().isoformat()
    }
    
    # Remove if already exists
    st.session_state.search_history = [
        h for h in st.session_state.search_history 
        if h['title'].lower() != movie_title.lower()
    ]
    
    # Add to beginning
    st.session_state.search_history.insert(0, history_item)
    
    # Keep only last MAX_HISTORY items
    st.session_state.search_history = st.session_state.search_history[:MAX_HISTORY]


def remove_from_history(movie_title):
    """Removes a movie from search history."""
    st.session_state.search_history = [
        h for h in st.session_state.search_history 
        if h['title'].lower() != movie_title.lower()
    ]


def add_to_favorites(movie_title, movie_data):
    """Adds a movie to favorites."""
    
    favorite_item = {
        'title': movie_title,
        'year': movie_data.get('Year', 'N/A'),
        'poster': movie_data.get('Poster', ''),
        'imdb_rating': movie_data.get('imdbRating', 'N/A')
    }
    
    # Check if already in favorites
    for fav in st.session_state.favorites:
        if fav['title'].lower() == movie_title.lower():
            return False  # Already exists
    
    st.session_state.favorites.insert(0, favorite_item)
    st.session_state.favorites = st.session_state.favorites[:MAX_FAVORITES]
    return True


def remove_from_favorites(movie_title):
    """Removes a movie from favorites."""
    st.session_state.favorites = [
        f for f in st.session_state.favorites 
        if f['title'].lower() != movie_title.lower()
    ]


def is_favorite(movie_title):
    """Checks if a movie is in favorites."""
    return any(f['title'].lower() == movie_title.lower() for f in st.session_state.favorites)


def clear_search():
    """Clears the current search."""
    st.session_state.search_query = ''
    st.session_state.current_movie = None
    st.session_state.search_suggestions = []


@st.cache_data
def get_poster_color(poster_url):
    """Extracts the average color from a movie poster."""
    
    try:
        response = requests.get(poster_url, timeout=10)
        image = Image.open(io.BytesIO(response.content))
        image_array = np.array(image).reshape(-1, 3)
        average_color = np.mean(image_array, axis=0)
        return tuple(int(c) for c in average_color)
    except:
        return (10, 10, 20)


def set_background_from_poster(color):
    """Sets a dynamic background gradient based on poster color."""
    
    gradient_css = f"""
    <style>
        .stApp {{
            background: linear-gradient(
                135deg,
                rgba({color[0]}, {color[1]}, {color[2]}, 0.15) 0%,
                #0a0a0f 30%,
                #1a0a2e 70%,
                rgba({color[0]}, {color[1]}, {color[2]}, 0.1) 100%
            );
            background-attachment: fixed;
        }}
    </style>
    """
    st.markdown(gradient_css, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#                              GENRE MAPPING
# ═══════════════════════════════════════════════════════════════════════════════

GENRES = {
    'All': None,
    'Action': 28,
    'Comedy': 35,
    'Drama': 18,
    'Horror': 27,
    'Sci-Fi': 878,
    'Romance': 10749,
    'Thriller': 53,
    'Animation': 16,
    'Documentary': 99,
    'Fantasy': 14
}


# ═══════════════════════════════════════════════════════════════════════════════
#                           ENHANCED SIDEBAR COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def show_enhanced_sidebar():
    """
    Creates and displays the enhanced sidebar with:
    - Real-time search with suggestions
    - Search history
    - Favorites
    - Trending movies
    - Genre filters
    - Year filters
    """
    
    with st.sidebar:
        # ═══════ LOGO/HEADER ═══════
        st.markdown("""
            <div style="text-align: center; padding: 15px 0;">
                <h1 style="font-size: 22px; margin: 0; letter-spacing: 3px;">🎬 CINEMAVERSE</h1>
                <p style="color: #666; font-size: 10px; margin: 5px 0; letter-spacing: 2px;">v2.1 QUANTUM SEARCH</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ═══════ NAVIGATION TABS ═══════
        nav_cols = st.columns(4)
        
        sections = [
            ('🔍', 'search', 'Search'),
            ('📜', 'history', 'History'),
            ('⭐', 'favorites', 'Favs'),
            ('🔥', 'trending', 'Hot')
        ]
        
        for i, (icon, key, label) in enumerate(sections):
            with nav_cols[i]:
                if st.button(icon, key=f"nav_{key}", help=label, use_container_width=True):
                    st.session_state.sidebar_section = key
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ═══════ SECTION CONTENT ═══════
        current_section = st.session_state.sidebar_section
        
        if current_section == 'search':
            show_search_section()
        elif current_section == 'history':
            show_history_section()
        elif current_section == 'favorites':
            show_favorites_section()
        elif current_section == 'trending':
            show_trending_section()
        
        # ═══════ STATS BAR ═══════
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        stats_cols = st.columns(3)
        with stats_cols[0]:
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-family: 'Orbitron'; font-size: 16px; color: #00f5ff;">
                        {len(st.session_state.search_history)}
                    </div>
                    <div style="font-size: 9px; color: #666;">SEARCHES</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[1]:
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-family: 'Orbitron'; font-size: 16px; color: #bf00ff;">
                        {len(st.session_state.favorites)}
                    </div>
                    <div style="font-size: 9px; color: #666;">FAVORITES</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stats_cols[2]:
            st.markdown("""
                <div style="text-align: center;">
                    <div style="font-family: 'Orbitron'; font-size: 16px; color: #ff006e;">∞</div>
                    <div style="font-size: 9px; color: #666;">MOVIES</div>
                </div>
            """, unsafe_allow_html=True)
        
        # ═══════ FOOTER ═══════
        st.markdown("""
            <div style="text-align: center; padding: 20px 0 10px 0; color: #333; font-size: 9px;">
                <p>Powered by OMDB • TMDB • YouTube</p>
                <p style="color: #444;">© 2024 CINEMAVERSE</p>
            </div>
        """, unsafe_allow_html=True)


def show_search_section():
    """Shows the search section in sidebar."""
    
    st.markdown("""
        <div class="sidebar-section-header">
            <span>🔍</span>
            <span>SEARCH MATRIX</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Search input with real-time suggestions
    search_query = st.text_input(
        "Search Movies",
        value=st.session_state.search_query,
        placeholder="Type movie name...",
        key="search_input",
        label_visibility="collapsed",
        on_change=lambda: update_suggestions()
    )
    
    # Keyboard shortcut hint
    st.markdown("""
        <p class="keyboard-hint">
            Press <span class="kbd">Enter</span> to search
        </p>
    """, unsafe_allow_html=True)
    
    # Update query in session state
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
    
    # Action buttons row
    btn_cols = st.columns([2, 1])
    
    with btn_cols[0]:
        search_clicked = st.button("⚡ ANALYZE", type="primary", use_container_width=True)
    
    with btn_cols[1]:
        if st.button("✕", use_container_width=True, help="Clear search"):
            clear_search()
            st.rerun()
    
    # Show suggestions if query exists
    if search_query and len(search_query) >= 2:
        suggestions = fetch_search_suggestions(search_query)
        
        if suggestions:
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #666; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">
                    💡 Suggestions
                </p>
            """, unsafe_allow_html=True)
            
            for sug in suggestions[:5]:
                col_poster, col_info = st.columns([1, 3])
                
                with col_poster:
                    if sug['poster']:
                        st.image(sug['poster'], width=40)
                    else:
                        st.markdown("🎬")
                
                with col_info:
                    if st.button(
                        f"{sug['title'][:25]}{'...' if len(sug['title']) > 25 else ''} ({sug['year']})",
                        key=f"sug_{sug['id']}",
                        use_container_width=True
                    ):
                        st.session_state.search_query = sug['title']
                        st.session_state.should_search = True
                        st.rerun()
    
    # Advanced filters (collapsible)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    with st.expander("🎛️ ADVANCED FILTERS"):
        # Genre filter
        selected_genre = st.selectbox(
            "Genre",
            options=list(GENRES.keys()),
            index=list(GENRES.keys()).index(st.session_state.selected_genre)
        )
        st.session_state.selected_genre = selected_genre
        
        # Year range filter
        current_year = datetime.now().year
        year_range = st.slider(
            "Year Range",
            min_value=1900,
            max_value=current_year,
            value=st.session_state.year_range,
            step=1
        )
        st.session_state.year_range = year_range
        
        # Apply filters button
        if st.button("Apply Filters", use_container_width=True):
            st.info("Filters applied! Search for a movie to see filtered results.")
    
    # Return search action
    return search_query, search_clicked


def show_history_section():
    """Shows the search history section in sidebar."""
    
    st.markdown("""
        <div class="sidebar-section-header">
            <span>📜</span>
            <span>SEARCH HISTORY</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.search_history:
        # Clear all button
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.search_history = []
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for item in st.session_state.search_history:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(
                    f"🎬 {item['title']} ({item['year']})",
                    key=f"hist_{item['title']}_{item['timestamp']}",
                    use_container_width=True
                ):
                    st.session_state.search_query = item['title']
                    st.session_state.should_search = True
                    st.session_state.sidebar_section = 'search'
                    st.rerun()
            
            with col2:
                if st.button("✕", key=f"del_hist_{item['title']}_{item['timestamp']}", help="Remove"):
                    remove_from_history(item['title'])
                    st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; padding: 30px 0; color: #555;">
                <p style="font-size: 32px;">📜</p>
                <p>No search history yet.</p>
                <p style="font-size: 12px;">Search for a movie to start!</p>
            </div>
        """, unsafe_allow_html=True)


def show_favorites_section():
    """Shows the favorites section in sidebar."""
    
    st.markdown("""
        <div class="sidebar-section-header">
            <span>⭐</span>
            <span>MY FAVORITES</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.favorites:
        for item in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                rating_display = f"⭐{item['imdb_rating']}" if item['imdb_rating'] != 'N/A' else ''
                if st.button(
                    f"🎬 {item['title'][:20]} {rating_display}",
                    key=f"fav_{item['title']}",
                    use_container_width=True
                ):
                    st.session_state.search_query = item['title']
                    st.session_state.should_search = True
                    st.session_state.sidebar_section = 'search'
                    st.rerun()
            
            with col2:
                if st.button("✕", key=f"del_fav_{item['title']}", help="Remove from favorites"):
                    remove_from_favorites(item['title'])
                    st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; padding: 30px 0; color: #555;">
                <p style="font-size: 32px;">⭐</p>
                <p>No favorites yet.</p>
                <p style="font-size: 12px;">Click the ⭐ icon on any movie!</p>
            </div>
        """, unsafe_allow_html=True)


def show_trending_section():
    """Shows the trending movies section in sidebar."""
    
    st.markdown("""
        <div class="sidebar-section-header">
            <span>🔥</span>
            <span>TRENDING NOW</span>
        </div>
    """, unsafe_allow_html=True)
    
    trending = fetch_trending_movies()
    
    if trending:
        for i, movie in enumerate(trending, 1):
            col_rank, col_info = st.columns([1, 4])
            
            with col_rank:
                st.markdown(f"""
                    <div style="
                        font-family: 'Orbitron', sans-serif;
                        font-size: 16px;
                        font-weight: 700;
                        color: {'#ff006e' if i <= 3 else '#bf00ff'};
                        text-align: center;
                        padding: 10px 0;
                    ">
                        #{i}
                    </div>
                """, unsafe_allow_html=True)
            
            with col_info:
                if st.button(
                    f"{movie['title'][:22]}{'...' if len(movie['title']) > 22 else ''} ⭐{movie['rating']}",
                    key=f"trend_{movie['id']}",
                    use_container_width=True
                ):
                    st.session_state.search_query = movie['title']
                    st.session_state.should_search = True
                    st.session_state.sidebar_section = 'search'
                    st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; padding: 30px 0; color: #555;">
                <p style="font-size: 32px;">🔥</p>
                <p>Could not load trending movies.</p>
                <p style="font-size: 12px;">Check your connection.</p>
            </div>
        """, unsafe_allow_html=True)


def update_suggestions():
    """Updates search suggestions based on current query."""
    query = st.session_state.get('search_input', '')
    if query and len(query) >= 2:
        st.session_state.search_suggestions = fetch_search_suggestions(query)
    else:
        st.session_state.search_suggestions = []


# ═══════════════════════════════════════════════════════════════════════════════
#                              UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def show_welcome_screen():
    """Displays the welcome screen when no movie is searched."""
    
    st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <div class="welcome-title">CinemaVerse</div>
            <p style="font-size: 18px; color: #888; margin-bottom: 40px;">
                🎬 Your Gateway to the Future of Movie Discovery 🚀
            </p>
            <div style="max-width: 600px; margin: 0 auto;">
                <p style="color: #666; font-size: 15px; line-height: 2;">
                    Enter a movie title in the sidebar to unlock:<br><br>
                    ⚡ <span style="color: #00f5ff;">Instant Movie Analytics</span><br>
                    🎥 <span style="color: #bf00ff;">HD Trailer Streaming</span><br>
                    📺 <span style="color: #ff006e;">Live Streaming Availability</span><br>
                    🤖 <span style="color: #00f5ff;">AI-Powered Recommendations</span><br>
                    🔥 <span style="color: #ff9500;">Trending Movies</span><br>
                    ⭐ <span style="color: #ffd700;">Personal Favorites</span>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Show some trending movies on welcome screen
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>🔥 Trending This Week</h3>", unsafe_allow_html=True)
    
    trending = fetch_trending_movies()
    if trending:
        cols = st.columns(5)
        for i, movie in enumerate(trending[:5]):
            with cols[i]:
                movie_id = movie['id']
                st.markdown(f"""
                    <div style="text-align: center; color: #00f5ff; font-weight: bold; font-size: 12px; margin-bottom: 8px;">
                        ⭐ {movie['rating']}/10
                    </div>
                """, unsafe_allow_html=True)
                
                if movie['poster']:
                    st.image(movie['poster'].replace('/w92/', '/w200/'), use_container_width=True)
                else:
                    st.markdown("🎬")
                    
                st.caption(movie['title'][:15] + "..." if len(movie['title']) > 15 else movie['title'])
                
                if st.button("📽️ View", key=f"welcome_trend_{movie_id}", use_container_width=True):
                    st.session_state.search_query = movie['title']
                    st.session_state.should_search = True
                    st.rerun()


def show_movie_header(movie_data):
    """Displays the main movie header with poster and basic info."""
    
    col_poster, col_info = st.columns([1, 2], gap="large")
    
    with col_poster:
        poster_url = movie_data.get('Poster', '')
        if poster_url and poster_url != 'N/A':
            st.markdown(f'''
                <div style="text-align: center;">
                    <img src="{poster_url}" class="movie-poster" style="max-width: 100%; height: auto;">
                </div>
            ''', unsafe_allow_html=True)
    
    with col_info:
        title = movie_data.get('Title', 'Unknown')
        year = movie_data.get('Year', 'N/A')
        
        # Title with favorite button
        title_col, fav_col = st.columns([5, 1])
        
        with title_col:
            st.markdown(f"""
                <h1 style="font-size: 36px; margin-bottom: 5px;">{title}</h1>
                <p style="color: #00f5ff; font-size: 20px; margin-bottom: 20px;">{year}</p>
            """, unsafe_allow_html=True)
        
        with fav_col:
            is_fav = is_favorite(title)
            fav_icon = "⭐" if is_fav else "☆"
            fav_help = "Remove from favorites" if is_fav else "Add to favorites"
            
            if st.button(fav_icon, key="fav_btn", help=fav_help):
                if is_fav:
                    remove_from_favorites(title)
                    st.toast(f"Removed '{title}' from favorites")
                else:
                    add_to_favorites(title, movie_data)
                    st.toast(f"Added '{title}' to favorites! ⭐")
                st.rerun()
        
        # Tagline
        tagline = movie_data.get('tagline') or movie_data.get('Tagline', '')
        if tagline:
            st.markdown(f'<p style="color: #888; font-style: italic; font-size: 16px;">"{tagline}"</p>', unsafe_allow_html=True)
        
        # Plot
        plot = movie_data.get('Plot', 'No plot available.')
        st.markdown(f'<p style="color: #ccc; line-height: 1.8; margin: 20px 0;">{plot}</p>', unsafe_allow_html=True)
        
        # Quick info row
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        info_cols = st.columns(3)
        
        with info_cols[0]:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{movie_data.get('imdbRating', 'N/A')}</div>
                    <div class="stat-label">⭐ IMDb Rating</div>
                </div>
            """, unsafe_allow_html=True)
        
        with info_cols[1]:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{movie_data.get('Metascore', 'N/A')}</div>
                    <div class="stat-label">🎯 Metascore</div>
                </div>
            """, unsafe_allow_html=True)
        
        with info_cols[2]:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{movie_data.get('Runtime', 'N/A')}</div>
                    <div class="stat-label">⏱️ Runtime</div>
                </div>
            """, unsafe_allow_html=True)


def show_movie_details(movie_data):
    """Displays additional movie details."""
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    details = [
        ("🎬 Director", movie_data.get('Director', 'N/A')),
        ("✍️ Writer", movie_data.get('Writer', 'N/A')[:50] + "..." if len(movie_data.get('Writer', '')) > 50 else movie_data.get('Writer', 'N/A')),
        ("🎭 Genre", movie_data.get('Genre', 'N/A')),
        ("🌍 Country", movie_data.get('Country', 'N/A'))
    ]
    
    for i, (label, value) in enumerate(details):
        with cols[i]:
            st.markdown(f"""
                <div style="padding: 15px;">
                    <p class="info-label">{label}</p>
                    <p class="info-value">{value}</p>
                </div>
            """, unsafe_allow_html=True)
    
    cast = movie_data.get('Actors', 'N/A')
    st.markdown(f"""
        <div style="padding: 15px 0;">
            <p class="info-label">🌟 Starring</p>
            <p class="info-value">{cast}</p>
        </div>
    """, unsafe_allow_html=True)


def show_trailer_tab(movie_data):
    """Displays the trailer tab content."""
    
    trailer_url = fetch_youtube_trailer(movie_data.get('Title', ''), movie_data.get('Year', ''))
    
    if trailer_url:
        st.video(trailer_url)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: #888;">
                <p style="font-size: 48px;">🎬</p>
                <p>Official trailer not available at this time.</p>
            </div>
        """, unsafe_allow_html=True)


def show_streaming_tab(movie_data):
    """Displays the streaming availability tab."""
    
    sources = fetch_streaming_info(movie_data.get('imdbID'))
    
    if sources:
        st.markdown("### 📺 Available on Subscription Services")
        st.markdown("<br>", unsafe_allow_html=True)
        
        badges_html = ""
        for source in sources:
            badges_html += f'<a href="{source["url"]}" target="_blank" class="streaming-badge">{source["name"]}</a>'
        
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: #888;">
                <p style="font-size: 48px;">📺</p>
                <p>Not currently available on major streaming platforms.</p>
                <p style="font-size: 12px; color: #555;">Try rental or purchase options.</p>
            </div>
        """, unsafe_allow_html=True)


def show_recommendations_tab(movie_data):
    """Displays the recommendations tab with improved movie cards."""
    
    recommendations = fetch_recommendations(movie_data.get('tmdb_id'))
    
    if recommendations:
        st.markdown("### 🤖 AI Recommendations")
        st.markdown("<br>", unsafe_allow_html=True)
        
        cols = st.columns(6)
        
        for i, rec in enumerate(recommendations[:6]):
            with cols[i]:
                poster_path = rec.get('poster_path')
                title = rec.get('title', 'Unknown')
                rating = rec.get('vote_average', 'N/A')
                rec_id = rec.get('id', i)
                
                # Movie card container
                st.markdown(f"""
                    <div style="background: rgba(15, 15, 25, 0.6); border: 1px solid rgba(0, 245, 255, 0.2); border-radius: 12px; padding: 12px; text-align: center;">
                        <div style="font-size: 12px; color: #00f5ff; margin-bottom: 6px; font-weight: bold;">⭐ {rating}/10</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}"
                    st.image(poster_url, use_container_width=True)
                else:
                    st.markdown("🎬 No Poster")
                
                st.caption(title[:25] + "..." if len(title) > 25 else title)
                
                # View Details button - creates a key that will navigate to the movie
                if st.button("📽️ View", key=f"rec_{rec_id}", use_container_width=True):
                    st.session_state.search_query = title
                    st.session_state.should_search = True
                    st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: #888;">
                <p style="font-size: 48px;">🤖</p>
                <p>No recommendations available at this time.</p>
            </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#                              MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main function that runs the entire application."""
    
    # Apply theme
    apply_futuristic_theme()
    
    # Show enhanced sidebar
    show_enhanced_sidebar()
    
    # Get initial search parameters - these come from session state which is updated by button clicks
    search_query = st.session_state.search_query
    should_search = st.session_state.should_search
    
    # Add a main search bar at the top
    st.markdown("""
        <div style="margin-bottom: 30px;">
            <h2 style="text-align: center; color: #00f5ff; margin-bottom: 20px;">🎬 CINEMAVERSE EXPLORER</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Search input at top
    top_search_col1, top_search_col2, top_search_col3 = st.columns([4, 1, 1])
    
    with top_search_col1:
        top_search = st.text_input(
            "Search any movie title...",
            value=search_query,
            placeholder="Enter movie name (e.g., Inception, Dune, Avatar)",
            label_visibility="collapsed",
            key="main_search_input"
        )
    
    with top_search_col2:
        top_search_btn = st.button("🔍 Search", use_container_width=True, type="primary", key="main_search_btn")
    
    with top_search_col3:
        if st.button("Clear", use_container_width=True, key="main_clear_btn"):
            st.session_state.search_query = ''
            st.session_state.current_movie = None
            st.session_state.search_suggestions = []
            st.session_state.should_search = False
            st.rerun()
    
    # Handle search - note: when top search button is clicked, we update state and must check top_search input
    if top_search_btn and top_search:
        st.session_state.search_query = top_search
        st.session_state.should_search = True
    
    # Determine final query to search for
    if st.session_state.should_search:
        final_query = st.session_state.search_query
        trigger_search = True
    elif top_search_btn and top_search:
        final_query = top_search
        trigger_search = True
    else:
        final_query = search_query
        trigger_search = False
    
    # Main content area - display movie if search is triggered
    if trigger_search and final_query:
        # Reset the search flag AFTER we've used it
        st.session_state.should_search = False
        
        with st.spinner("🔮 Accessing the Movie Matrix..."):
            movie_data, error = fetch_movie_data(final_query)
        
        if error:
            st.error(error)
            st.markdown("""
                <div style="text-align: center; padding: 30px;">
                    <p style="color: #888;">Try searching for another movie or check your spelling.</p>
                </div>
            """, unsafe_allow_html=True)
        
        elif movie_data:
            # Add to history
            add_to_history(movie_data.get('Title', final_query), movie_data)
            
            # Set dynamic background
            poster_url = movie_data.get('Poster', '')
            if poster_url and poster_url != 'N/A':
                poster_color = get_poster_color(poster_url)
                set_background_from_poster(poster_color)
            
            # Main content container
            st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
            
            show_movie_header(movie_data)
            show_movie_details(movie_data)
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Tabs
            tab_trailer, tab_streaming, tab_recs = st.tabs([
                "🎬 TRAILER",
                "📺 STREAMING",
                "🤖 SIMILAR"
            ])
            
            with tab_trailer:
                show_trailer_tab(movie_data)
            
            with tab_streaming:
                show_streaming_tab(movie_data)
            
            with tab_recs:
                show_recommendations_tab(movie_data)
            
            # Raw data expander
            with st.expander("📊 View Raw Data Matrix"):
                st.json(movie_data)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif final_query and not trigger_search:
        # User is typing but hasn't pressed search yet
        # Show a hint
        st.markdown(f"""
            <div style="text-align: center; padding: 100px 20px; color: #666;">
                <p style="font-size: 24px;">Press <span style="color: #00f5ff;">⚡ Search</span> to search for:</p>
                <p style="font-size: 32px; color: #fff; font-family: 'Orbitron', sans-serif;">{final_query}</p>
            </div>
        """, unsafe_allow_html=True)
    
    else:
        # Show welcome screen
        show_welcome_screen()


# ═══════════════════════════════════════════════════════════════════════════════
#                              RUN THE APP
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()