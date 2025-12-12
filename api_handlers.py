# ═══════════════════════════════════════════════════════════════════════════════
#                          API HANDLERS MODULE
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
import requests
from typing import Dict, Optional, List, Tuple
from config import API_KEYS


@st.cache_data(ttl=3600)
def fetch_movie_data(movie_title: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Fetches movie information from OMDB and TMDB APIs.
    
    Args:
        movie_title: Title of the movie to search for
        
    Returns:
        Tuple of (movie_data_dict, error_message)
    """
    try:
        # OMDB API call
        omdb_url = f"http://www.omdbapi.com/?t={movie_title}&plot=full&apikey={API_KEYS['omdb']}"
        omdb_response = requests.get(omdb_url, timeout=15)
        omdb_data = omdb_response.json()
        
        if omdb_data.get('Response') == 'False':
            return None, f"❌ Movie '{movie_title}' not found. Try checking the spelling!"
        
        movie_data = omdb_data
        imdb_id = movie_data.get('imdbID')
        
        # Try to fetch additional data from TMDB
        if imdb_id and API_KEYS['tmdb']:
            try:
                tmdb_find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={API_KEYS['tmdb']}&external_source=imdb_id"
                tmdb_response = requests.get(tmdb_find_url, timeout=15)
                tmdb_data = tmdb_response.json()
                
                if tmdb_data.get('movie_results'):
                    tmdb_id = tmdb_data['movie_results'][0]['id']
                    tmdb_details_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEYS['tmdb']}"
                    tmdb_details = requests.get(tmdb_details_url, timeout=15).json()
                    movie_data = {**tmdb_details, **movie_data}
                    movie_data['tmdb_id'] = tmdb_id
            except:
                pass  # Continue with OMDB data only
        
        return movie_data, None
        
    except requests.exceptions.Timeout:
        return None, "⏱️ Connection timed out. Please try again!"
    except requests.exceptions.RequestException as error:
        return None, f"🌐 Network error: {error}"


@st.cache_data(ttl=300)
def fetch_search_suggestions(query: str) -> List[Dict]:
    """
    Fetches search suggestions as user types using TMDB API.
    
    Args:
        query: Search query string
        
    Returns:
        List of suggestion dictionaries
    """
    if not query or len(query) < 2:
        return []
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEYS['tmdb']}&query={query}&page=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        suggestions = []
        for movie in data.get('results', [])[:8]:
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
def fetch_trending_movies() -> List[Dict]:
    """
    Fetches trending movies from TMDB API.
    
    Returns:
        List of trending movie dictionaries
    """
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
def fetch_movies_by_genre(genre_id: int) -> List[Dict]:
    """
    Fetches movies by genre from TMDB API.
    
    Args:
        genre_id: TMDB genre ID
        
    Returns:
        List of movie dictionaries
    """
    try:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEYS['tmdb']}&with_genres={genre_id}&sort_by=popularity.desc"
        response = requests.get(url, timeout=10)
        return response.json().get('results', [])[:10]
    except:
        return []


@st.cache_data(ttl=3600)
def fetch_recommendations(tmdb_id: int) -> List[Dict]:
    """
    Gets similar movie recommendations from TMDB API.
    
    Args:
        tmdb_id: TMDB movie ID
        
    Returns:
        List of recommendation movie dictionaries
    """
    if not tmdb_id:
        return []
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/recommendations?api_key={API_KEYS['tmdb']}"
        response = requests.get(url, timeout=10)
        return response.json().get('results', [])
    except:
        return []


@st.cache_data(ttl=86400)
def fetch_streaming_info(imdb_id: str) -> List[Dict]:
    """
    Gets streaming availability information from Watchmode API.
    
    Args:
        imdb_id: IMDb ID of the movie
        
    Returns:
        List of streaming source dictionaries
    """
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
def fetch_youtube_trailer(title: str, year: str) -> Optional[str]:
    """
    Searches YouTube for the official movie trailer.
    
    Args:
        title: Movie title
        year: Movie year
        
    Returns:
        YouTube trailer URL or None
    """
    try:
        from googleapiclient.discovery import build
        
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
