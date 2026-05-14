import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://api.football-data.org/v4"

headers = {
    "X-Auth-Token": API_KEY
}

def get_competition_teams(competition_code, season=None):

    url = f"{BASE_URL}/competitions/{competition_code}/teams"

    params = {}

    if season:
        params["season"] = season

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["teams"]

def get_competition_matches(competition_code, season=None):

    url = f"{BASE_URL}/competitions/{competition_code}/matches"

    params = {}

    if season:
        params["season"] = season

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["matches"]