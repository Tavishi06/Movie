# ═══════════════════════════════════════════════════════════════════════════════
#                          SESSION STATE MANAGER MODULE
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
from config import SESSION_STATE_DEFAULTS


def init_session_state():
    """Initialize all session state variables."""
    for key, value in SESSION_STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_search_query():
    """Get current search query from session state."""
    return st.session_state.get('search_query', '')


def set_search_query(query: str):
    """Set search query in session state."""
    st.session_state.search_query = query


def should_trigger_search():
    """Check if search should be triggered."""
    return st.session_state.get('should_search', False)


def set_should_search(value: bool):
    """Set the should_search flag."""
    st.session_state.should_search = value


def add_to_history(movie_title: str, movie_data: dict):
    """Add a movie to search history."""
    history = st.session_state.search_history
    
    # Remove if already exists to avoid duplicates
    history = [m for m in history if m.get('title') != movie_title]
    
    # Add to beginning
    history.insert(0, {
        'title': movie_title,
        'poster': movie_data.get('Poster', ''),
        'year': movie_data.get('Year', ''),
        'imdb_id': movie_data.get('imdbID', '')
    })
    
    # Keep only last 10
    st.session_state.search_history = history[:10]


def add_to_favorites(movie_title: str, movie_data: dict):
    """Add a movie to favorites."""
    favorites = st.session_state.favorites
    
    # Check if already in favorites
    if any(m.get('title') == movie_title for m in favorites):
        return False
    
    favorites.append({
        'title': movie_title,
        'poster': movie_data.get('Poster', ''),
        'imdb_id': movie_data.get('imdbID', ''),
        'rating': movie_data.get('imdbRating', 'N/A')
    })
    
    # Keep only last 20
    st.session_state.favorites = favorites[:20]
    return True


def is_favorite(movie_title: str) -> bool:
    """Check if a movie is in favorites."""
    return any(m.get('title') == movie_title for m in st.session_state.favorites)


def remove_from_favorites(movie_title: str):
    """Remove a movie from favorites."""
    st.session_state.favorites = [
        m for m in st.session_state.favorites 
        if m.get('title') != movie_title
    ]


def clear_history():
    """Clear search history."""
    st.session_state.search_history = []


def clear_favorites():
    """Clear all favorites."""
    st.session_state.favorites = []


def reset_search():
    """Reset search state."""
    st.session_state.search_query = ''
    st.session_state.current_movie = None
    st.session_state.search_suggestions = []
    st.session_state.should_search = False
