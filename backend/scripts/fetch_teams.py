from sqlalchemy.orm import sessionmaker

from database.db import engine
from database.models import Team

from services.fdata_service import get_premier_league_teams

Session = sessionmaker(bind=engine)
session = Session()

teams = get_premier_league_teams()

for team in teams:

    existing_team = session.query(Team).filter_by(
        api_team_id=team["id"]
    ).first()

    if existing_team:
        continue

    new_team = Team(
        api_team_id=team["id"],
        name=team["name"],
        short_name=team["shortName"],
        tla=team["tla"],
        country=team["area"]["name"]
    )

    session.add(new_team)

session.commit()

print("Equipos guardados correctamente")