# ═══════════════════════════════════════════════════════════════════════════════
#                              CONFIGURATION MODULE
# ═══════════════════════════════════════════════════════════════════════════════

from datetime import datetime

# API Keys Configuration
API_KEYS = {
    "omdb": "b501ccee",
    "tmdb": "5ad127b6be5b77aa124a8c1743dd33e7",
    "youtube": "AIzaSyBwB_Ls-jh-9KmVtirmUueQAFC8OG5uPzM",
    "watchmode": "8e4svmLGGt4J6vyCqMMrcAu4OoIWg3ETaz4Mzsxq"
}

# API Endpoints
OMDB_BASE_URL = "https://www.omdbapi.com/"
TMDB_BASE_URL = "https://api.themoviedb.org/3/"
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3/"
WATCHMODE_BASE_URL = "https://api.watchmode.com/v1/"

# Application Settings
MAX_HISTORY = 10
MAX_FAVORITES = 20
CACHE_TTL = 3600  # 1 hour
TRENDING_CACHE_TTL = 300  # 5 minutes

# UI Configuration
APP_TITLE = "CinemaVerse"
APP_SUBTITLE = "Explore the Universe of Movies"
APP_ICON = "🎬"

# Color Theme
COLORS = {
    "neon_blue": "#00f5ff",
    "neon_purple": "#bf00ff",
    "neon_pink": "#ff006e",
    "neon_green": "#00ff88",
    "neon_orange": "#ff9500",
    "dark_bg": "#0a0a0f",
    "card_bg": "rgba(15, 15, 25, 0.9)",
    "glass_bg": "rgba(255, 255, 255, 0.05)",
    "border_glow": "rgba(0, 245, 255, 0.3)"
}

# Fonts
FONTS = {
    "header": "'Orbitron', sans-serif",
    "body": "'Rajdhani', sans-serif"
}

# Session State Defaults
SESSION_STATE_DEFAULTS = {
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
    'sidebar_section': 'search'
}
