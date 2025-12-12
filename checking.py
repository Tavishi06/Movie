import requests

# --- YOUR KEYS ---
OMDB_API_KEY = "b501ccee"
WATCHMODE_API_KEY = "8e4svmLGGt4J6vyCqMMrcAu4OoIWg3ETaz4Mzsxq"
YOUTUBE_API_KEY = "AIzaSyBwB_Ls-jh-9KmVtirmUueQAFC8OG5uPzM" 
TMDB_API_KEY = "5ad127b6be5b77aa124a8c1743dd33e7"

def check_omdb(api_key):
    # Endpoint: Search for "Inception"
    url = f"http://www.omdbapi.com/?apikey={api_key}&t=Inception"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get('Response') == "True":
            return "✅ VALID"
        else:
            return f"❌ INVALID (Error: {data.get('Error', 'Unknown')})"
    except Exception as e:
        return f"⚠️ ERROR ({str(e)})"

def check_watchmode(api_key):
    # Endpoint: Get details for a specific title (Breaking Bad ID: 3173903)
    url = f"https://api.watchmode.com/v1/title/3173903/details/?apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "✅ VALID"
        elif response.status_code == 401:
            return "❌ INVALID (Unauthorized)"
        elif response.status_code == 402:
            return "❌ INVALID (Quota Exceeded)"
        else:
            return f"❌ INVALID (Status: {response.status_code})"
    except Exception as e:
        return f"⚠️ ERROR ({str(e)})"

def check_youtube(api_key):
    # Endpoint: Get details for a generic video ID
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id=dQw4w9WgXcQ&key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "✅ VALID"
        else:
            return f"❌ INVALID (Status: {response.status_code})"
    except Exception as e:
        return f"⚠️ ERROR ({str(e)})"

def check_tmdb(api_key):
    # Endpoint: Get details for Movie ID 550 (Fight Club)
    url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return "✅ VALID"
        else:
            return f"❌ INVALID (Status: {response.status_code})"
    except Exception as e:
        return f"⚠️ ERROR ({str(e)})"

# --- RUN CHECKS ---
print(f"OMDb Key:      {check_omdb(OMDB_API_KEY)}")
print(f"Watchmode Key: {check_watchmode(WATCHMODE_API_KEY)}")
print(f"YouTube Key:   {check_youtube(YOUTUBE_API_KEY)}")
print(f"TMDb Key:      {check_tmdb(TMDB_API_KEY)}")