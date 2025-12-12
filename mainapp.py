# ═══════════════════════════════════════════════════════════════════════════════
#                          CINEMAVERSE - MAIN APPLICATION
#                        Modular Movie Discovery Platform
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st

# Import all modules
from config import (
    APP_TITLE, APP_SUBTITLE, APP_ICON,
    COLORS, FONTS
)
from session_manager import (
    init_session_state, get_search_query, set_search_query,
    should_trigger_search, set_should_search, add_to_history,
    reset_search
)
from api_handlers import (
    fetch_movie_data, fetch_trending_movies
)
from ui_components import (
    apply_futuristic_theme, show_welcome_screen,
    show_movie_header, show_movie_details,
    show_trailer_tab, show_streaming_tab,
    show_recommendations_tab
)


# ═══════════════════════════════════════════════════════════════════════════════
#                              PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=f"{APP_TITLE} | {APP_SUBTITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()


# ═══════════════════════════════════════════════════════════════════════════════
#                              MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main function that orchestrates the entire application."""
    
    # Apply futuristic theme
    apply_futuristic_theme()
    
    # Get initial search parameters - these come from session state which is updated by button clicks
    search_query = get_search_query()
    should_search = should_trigger_search()
    
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
            reset_search()
            st.rerun()
    
    # Handle search - note: when top search button is clicked, we update state and must check top_search input
    if top_search_btn and top_search:
        set_search_query(top_search)
        set_should_search(True)
    
    # Determine final query to search for
    if should_trigger_search():
        final_query = get_search_query()
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
        set_should_search(False)
        
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

# ═══════════════════════════════════════════════════════════════════════════════
#                          CINEMAVERSE - MAIN APPLICATION
#                        Modular Movie Discovery Platform
# ═══════════════════════════════════════════════════════════════════════════════

import streamlit as st

# Import all modules
from config import (
    APP_TITLE, APP_SUBTITLE, APP_ICON,
    COLORS, FONTS
)
from session_manager import (
    init_session_state, get_search_query, set_search_query,
    should_trigger_search, set_should_search, add_to_history,
    reset_search
)
from api_handlers import (
    fetch_movie_data, fetch_trending_movies
)
from ui_components import (
    apply_futuristic_theme, show_welcome_screen,
    show_movie_header, show_movie_details,
    show_trailer_tab, show_streaming_tab,
    show_recommendations_tab
)


# ═══════════════════════════════════════════════════════════════════════════════
#                              PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=f"{APP_TITLE} | {APP_SUBTITLE}",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()


# ═══════════════════════════════════════════════════════════════════════════════
#                              MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main function that orchestrates the entire application."""
    
    # Apply futuristic theme
    apply_futuristic_theme()
    
    # Get initial search parameters - these come from session state which is updated by button clicks
    search_query = get_search_query()
    should_search = should_trigger_search()
    
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
            reset_search()
            st.rerun()
    
    # Handle search - note: when top search button is clicked, we update state and must check top_search input
    if top_search_btn and top_search:
        set_search_query(top_search)
        set_should_search(True)
    
    # Determine final query to search for
    if should_trigger_search():
        final_query = get_search_query()
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
        set_should_search(False)
        
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