from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database.db import engine
from database.models import Match, Team, Competition

from services.fdata_service import get_competition_matches

Session = sessionmaker(bind=engine)
session = Session()

competition_codes = [
    "PL",
    "PD",
    "SA",
    "BL1",
    "FL1"
]

seasons = [
    2020,
    2021,
    2022,
    2023,
    2024
]

for competition_code in competition_codes:

    competition = session.query(Competition).filter_by(
        code=competition_code
    ).first()

    if not competition:
        print(f"Competition {competition_code} not found")
        continue

    for season in seasons:

        print(f"Fetching {competition_code} - {season}")

        try:

            matches = get_competition_matches(
                competition_code,
                season
            )

            for match in matches:

                existing_match = session.query(Match).filter_by(
                    api_fixture_id=match["id"]
                ).first()

                if existing_match:
                    continue

                home_team = session.query(Team).filter_by(
                    api_team_id=match["homeTeam"]["id"]
                ).first()

                away_team = session.query(Team).filter_by(
                    api_team_id=match["awayTeam"]["id"]
                ).first()

                if not home_team or not away_team:
                    continue

                match_date = datetime.fromisoformat(
                    match["utcDate"].replace("Z", "+00:00")
                )

                referees = match.get("referees", [])

                referee_name = None

                if referees:
                    referee_name = referees[0].get("name")

                new_match = Match(
                    api_fixture_id=match["id"],

                    competition_id=competition.id,

                    season=season,

                    date=match_date,

                    home_team_id=home_team.id,
                    away_team_id=away_team.id,

                    home_goals=match["score"]["fullTime"]["home"],
                    away_goals=match["score"]["fullTime"]["away"],

                    status=match["status"],

                    referee=referee_name
                )

                session.add(new_match)

            session.commit()

            print(f"Completed {competition_code} {season}")

        except Exception as e:

            print(f"Error in {competition_code} {season}")
            print(e)