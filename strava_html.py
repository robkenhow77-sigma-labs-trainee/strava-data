from os import environ as ENV
from dotenv import load_dotenv

load_dotenv()
STRAVA_AUTH_URL = f"https://www.strava.com/oauth/authorize?client_id={ENV["CLIENT_ID"]}&redirect_uri=http://localhost:5000/callback&response_type=code&scope=activity:read_all"


HOME_PAGE = f"""
    <h1>Strava data project<h1/>
    <button onclick="window.location.href='{STRAVA_AUTH_URL}'">Go to google</button>
    """