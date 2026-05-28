from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

from database.db import engine
from database.models import Match, Team, Competition

from services.api_football_service import (
    get_matches_by_league_and_season
)

Session = sessionmaker(bind=engine)
session = Session()

competitions = {
    39: "Premier League",
    140: "La Liga",
    135: "Serie A",
    78: "Bundesliga",
    61: "Ligue 1",
    262: "Liga MX",
    94: "Primera Liga",
    88: "Eredivisie" 
}

seasons = [
    #2016,
    #2017,
    #2018,
    #2019,
    #2020,
    #2021,
    #2022,
    #2023,
    #2024,
    2025,
    2026
]

for league_id, league_name in competitions.items():

    competition = session.query(Competition).filter_by(
        api_league_id=league_id
    ).first()

    if not competition:
        print(f"Competition {league_name} not found")
        continue

    for season in seasons:

        print(f"Fetching {league_name} {season}")

        try:

            time.sleep(7)

            matches = get_matches_by_league_and_season(
                league_id,
                season
            )

            for match in matches:

                fixture = match["fixture"]
                teams = match["teams"]
                goals = match["goals"]
                league = match["league"]
                
                match_date = datetime.fromisoformat(
                    fixture["date"].replace("Z", "+00:00")
                )

                referee_name = fixture.get("referee")

                existing_match = session.query(Match).filter_by(
                    api_fixture_id=fixture["id"]
                ).first()

                if existing_match:

                    existing_match.status = (
                        fixture["status"]["short"]
                    )

                    existing_match.home_goals = (
                        goals["home"]
                    )

                    existing_match.away_goals = (
                        goals["away"]
                    )

                    existing_match.round = (
                        league.get("round")
                    )

                    existing_match.date = match_date

                    existing_match.referee = referee_name

                    continue

                home_team = session.query(Team).filter_by(
                    api_team_id=teams["home"]["id"]
                ).first()

                away_team = session.query(Team).filter_by(
                    api_team_id=teams["away"]["id"]
                ).first()

                if not home_team or not away_team:
                    continue

                new_match = Match(
                    api_fixture_id=fixture["id"],

                    competition_id=competition.id,

                    season=season,

                    round=league.get("round"),

                    date=match_date,

                    home_team_id=home_team.id,
                    away_team_id=away_team.id,

                    home_goals=goals["home"],
                    away_goals=goals["away"],

                    status=fixture["status"]["short"],

                    referee=referee_name
                )

                session.add(new_match)

            session.commit()

            print(f"Completed {league_name} {season}")

        except Exception as e:

            print(f"Error in {league_name} {season}")
            print(e)