import os
from urllib import response
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

def get_teams_by_league_and_season(league_id, season):

    url = f"{BASE_URL}/teams"

    params = {
        "league": league_id,
        "season": season
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )
    print(response.status_code)
    print(response.text)

    response.raise_for_status()

    data = response.json()

    return data["response"]

def get_matches_by_league_and_season(league_id, season):

    url = f"{BASE_URL}/fixtures"

    params = {
        "league": league_id,
        "season": season
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]

def get_match_statistics(fixture_id):

    url = f"{BASE_URL}/fixtures/statistics"

    params = {
        "fixture": fixture_id
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    print(response.status_code)

    response.raise_for_status()

    data = response.json()

    return data["response"]

def get_coaches_by_team(
    team_id
):

    url = f"{BASE_URL}/coachs"

    params = {
        "team": team_id
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]