
# ═══════════════════════════════════════════════════════════════════════════════
#                          UI COMPONENTS MODULE
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
from config import COLORS, FONTS
from api_handlers import fetch_trending_movies, fetch_search_suggestions, fetch_recommendations
from session_manager import (
    is_favorite, add_to_favorites, remove_from_favorites, add_to_history
)


def apply_futuristic_theme():
    """Applies the futuristic cyberpunk-inspired theme to the app."""
    
    futuristic_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
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
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
            background-attachment: fixed;
        }
        
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
        
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent);
            margin: 15px 0;
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
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    
    st.markdown(futuristic_css, unsafe_allow_html=True)


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
                    Enter a movie title in the search bar to unlock:<br><br>
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


def show_movie_header(movie_data: dict):
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
                    if add_to_favorites(title, movie_data):
                        st.toast(f"Added '{title}' to favorites!")


def show_movie_details(movie_data: dict):
    """Displays detailed movie information."""
    
    details = []
    
    if movie_data.get('imdbRating') and movie_data['imdbRating'] != 'N/A':
        details.append(f"⭐ Rating: {movie_data['imdbRating']}/10")
    
    if movie_data.get('Runtime') and movie_data['Runtime'] != 'N/A':
        details.append(f"⏱️ Runtime: {movie_data['Runtime']}")
    
    if movie_data.get('Genre') and movie_data['Genre'] != 'N/A':
        details.append(f"🎭 Genre: {movie_data['Genre']}")
    
    if movie_data.get('Director') and movie_data['Director'] != 'N/A':
        details.append(f"🎬 Director: {movie_data['Director'][:30]}")
    
    if movie_data.get('Plot') and movie_data['Plot'] != 'N/A':
        st.markdown(f"### Plot\n{movie_data['Plot']}")
    
    if details:
        st.markdown("<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>", unsafe_allow_html=True)
        for detail in details:
            st.markdown(f"<p style='color: #888;'>{detail}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def show_trailer_tab(movie_data: dict):
    """Displays trailer information in a tab."""
    
    from api_handlers import fetch_youtube_trailer
    
    title = movie_data.get('Title', '')
    year = movie_data.get('Year', '')
    
    with st.spinner("🔍 Searching for trailer..."):
        trailer_url = fetch_youtube_trailer(title, year)
    
    if trailer_url:
        st.markdown(f"🎬 [Watch Trailer on YouTube]({trailer_url})")
        st.success("Trailer found! Click the link to watch.")
    else:
        st.warning("Trailer not found. Try searching YouTube directly.")


def show_streaming_tab(movie_data: dict):
    """Displays streaming availability information."""
    
    from api_handlers import fetch_streaming_info
    
    imdb_id = movie_data.get('imdbID', '')
    
    if not imdb_id:
        st.warning("Streaming information not available.")
        return
    
    with st.spinner("🔍 Checking streaming platforms..."):
        sources = fetch_streaming_info(imdb_id)
    
    if sources:
        st.subheader("Available On:")
        for source in sources:
            st.markdown(f"📺 [{source['name']}]({source['url']})")
    else:
        st.info("Streaming availability could not be determined. Try checking the movie on Watchmode.")


def show_recommendations_tab(movie_data: dict):
    """Displays similar movie recommendations."""
    
    tmdb_id = movie_data.get('tmdb_id')
    
    if not tmdb_id:
        st.warning("Recommendations not available for this movie.")
        return
    
    recommendations = fetch_recommendations(tmdb_id)
    
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
#                          UI COMPONENTS MODULE
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st
from config import COLORS, FONTS
from api_handlers import fetch_trending_movies, fetch_search_suggestions, fetch_recommendations
from session_manager import (
    is_favorite, add_to_favorites, remove_from_favorites, add_to_history
)


def apply_futuristic_theme():
    """Applies the futuristic cyberpunk-inspired theme to the app."""
    
    futuristic_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
        
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
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a0f 100%);
            background-attachment: fixed;
        }
        
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
        
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent);
            margin: 15px 0;
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
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """
    
    st.markdown(futuristic_css, unsafe_allow_html=True)


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
                    Enter a movie title in the search bar to unlock:<br><br>
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


def show_movie_header(movie_data: dict):
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
                    if add_to_favorites(title, movie_data):
                        st.toast(f"Added '{title}' to favorites!")


def show_movie_details(movie_data: dict):
    """Displays detailed movie information."""
    
    details = []
    
    if movie_data.get('imdbRating') and movie_data['imdbRating'] != 'N/A':
        details.append(f"⭐ Rating: {movie_data['imdbRating']}/10")
    
    if movie_data.get('Runtime') and movie_data['Runtime'] != 'N/A':
        details.append(f"⏱️ Runtime: {movie_data['Runtime']}")
    
    if movie_data.get('Genre') and movie_data['Genre'] != 'N/A':
        details.append(f"🎭 Genre: {movie_data['Genre']}")
    
    if movie_data.get('Director') and movie_data['Director'] != 'N/A':
        details.append(f"🎬 Director: {movie_data['Director'][:30]}")
    
    if movie_data.get('Plot') and movie_data['Plot'] != 'N/A':
        st.markdown(f"### Plot\n{movie_data['Plot']}")
    
    if details:
        st.markdown("<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px;'>", unsafe_allow_html=True)
        for detail in details:
            st.markdown(f"<p style='color: #888;'>{detail}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def show_trailer_tab(movie_data: dict):
    """Displays trailer information in a tab."""
    
    from api_handlers import fetch_youtube_trailer
    
    title = movie_data.get('Title', '')
    year = movie_data.get('Year', '')
    
    with st.spinner("🔍 Searching for trailer..."):
        trailer_url = fetch_youtube_trailer(title, year)
    
    if trailer_url:
        st.markdown(f"🎬 [Watch Trailer on YouTube]({trailer_url})")
        st.success("Trailer found! Click the link to watch.")
    else:
        st.warning("Trailer not found. Try searching YouTube directly.")


def show_streaming_tab(movie_data: dict):
    """Displays streaming availability information."""
    
    from api_handlers import fetch_streaming_info
    
    imdb_id = movie_data.get('imdbID', '')
    
    if not imdb_id:
        st.warning("Streaming information not available.")
        return
    
    with st.spinner("🔍 Checking streaming platforms..."):
        sources = fetch_streaming_info(imdb_id)
    
    if sources:
        st.subheader("Available On:")
        for source in sources:
            st.markdown(f"📺 [{source['name']}]({source['url']})")
    else:
        st.info("Streaming availability could not be determined. Try checking the movie on Watchmode.")


def show_recommendations_tab(movie_data: dict):
    """Displays similar movie recommendations."""
    
    tmdb_id = movie_data.get('tmdb_id')
    
    if not tmdb_id:
        st.warning("Recommendations not available for this movie.")
        return
    
    recommendations = fetch_recommendations(tmdb_id)
    
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
