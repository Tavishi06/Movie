# CinemaVerse — Movie Discovery App

A Streamlit-powered movie discovery web application (**CinemaVerse**) that aggregates movie metadata, posters, search suggestions, and official trailers using the OMDb, TMDB, YouTube, and Watchmode APIs.

## Features

- **Live Search Suggestions**: Real-time movie autocomplete powered by TMDB (`fetch_search_suggestions`) with poster thumbnails, release year, and rating previews.
- **Detailed Movie Overview**: Combines OMDb and TMDB data (`fetch_movie_data`) to display the movie poster, IMDb rating, genre, runtime, director, cast, and full plot.
- **Official Trailer Playback**: Searches YouTube Data API v3 (`fetch_youtube_trailer`) and embeds the official trailer directly in the app via `st.video`.
- **Modular Architecture**: Includes reusable modules for session state history/favorites (`session_manager.py`), additional UI tabs such as streaming availability & recommendations (`ui_components.py`), and API health checking (`checking.py`).
- **Custom Cyber/Neon UI**: Styled with gradient backgrounds and `Orbitron` / `Rajdhani` typography.

## Tech Stack

- **Frontend / Framework**: Python, Streamlit
- **APIs**: OMDb API, TMDB API, YouTube Data API v3, Watchmode API
- **Libraries**: `streamlit`, `requests`, `pillow`, `python-dotenv`, `beautifulsoup4`

## Project Structure

```text
Movie/
├── mainapp.py           # Main Streamlit application entrypoint
├── config.py            # App metadata, API configuration, theme colors & session defaults
├── api_handlers.py      # Cached API helpers (OMDb, TMDB, Watchmode, YouTube)
├── ui_components.py     # Modular UI views (welcome screen, details, trailer, streaming, recommendations)
├── session_manager.py   # Search history and favorites state management
├── checking.py          # Script to validate API key connectivity
├── movie.py             # Alternate configuration module
├── test.py              # Earlier prototype script
└── requirements.txt     # Python package dependencies
```

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(If you use YouTube trailer search via `googleapiclient`, also install `google-api-python-client`.)*

2. Configure API credentials in `config.py` under `API_KEYS` (OMDb, TMDB, YouTube, Watchmode).

3. Launch the Streamlit app:
   ```bash
   streamlit run mainapp.py
   ```

4. *(Optional)* Verify API connectivity:
   ```bash
   python checking.py
   ```

## Contributors

| Contributor | GitHub | Role |
| --- | --- | --- |
| **Tavishi** | [@Tavishi06](https://github.com/Tavishi06) | Project Creator & Core Developer |
| **Tanish Jaswal** | [@WARRIORXR](https://github.com/WARRIORXR) | Documentation & Repository Contributor |
