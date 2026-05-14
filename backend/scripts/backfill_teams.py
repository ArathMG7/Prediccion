import time

from sqlalchemy.orm import sessionmaker

from database.db import engine
from database.models import Team

from services.api_football_service import (
    get_teams_by_league_and_season
)

Session = sessionmaker(bind=engine)
session = Session()

competitions = {
    39: "Premier League",
    140: "La Liga",
    135: "Serie A",
    78: "Bundesliga",
    61: "Ligue 1",
    262: "Liga MX"
}

seasons = [
    2020,
    2021,
    2022,
    2023,
    2024
]

for league_id, league_name in competitions.items():

    for season in seasons:

        print(f"Fetching {league_name} {season}")

        try:
            time.sleep(7)
            teams = get_teams_by_league_and_season(
                league_id,
                season
            )

            for item in teams:

                team_data = item["team"]
                venue_data = item["venue"]

                existing_team = session.query(Team).filter_by(
                    api_team_id=team_data["id"]
                ).first()

                if existing_team:
                    continue

                new_team = Team(
                    api_team_id=team_data["id"],

                    name=team_data["name"],

                    short_name=team_data.get("name"),

                    code=team_data.get("code"),

                    country=team_data.get("country"),

                    founded=team_data.get("founded"),

                    logo=team_data.get("logo"),

                    venue_name=venue_data.get("name"),

                    venue_city=venue_data.get("city"),

                    venue_capacity=venue_data.get("capacity")
                )

                session.add(new_team)

            session.commit()

            print(f"Completed {league_name} {season}")

        except Exception as e:

            print(f"Error in {league_name} {season}")
            print(e)