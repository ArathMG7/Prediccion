from sqlalchemy.orm import sessionmaker

from database.db import engine
from database.models import Competition

Session = sessionmaker(bind=engine)
session = Session()

competitions = [
    {
        "api_league_id": 39,
        "code": "PL",
        "name": "Premier League",
        "country": "England"
    },
    {
        "api_league_id": 140,
        "code": "PD",
        "name": "La Liga",
        "country": "Spain"
    },
    {
        "api_league_id": 135,
        "code": "SA",
        "name": "Serie A",
        "country": "Italy"
    },
    {
        "api_league_id": 78,
        "code": "BL1",
        "name": "Bundesliga",
        "country": "Germany"
    },
    {
        "api_league_id": 61,
        "code": "FL1",
        "name": "Ligue 1",
        "country": "France"
    },
    {
        "api_league_id": 262,
        "code": "MX",
        "name": "Liga MX",
        "country": "Mexico"
    },
    {
        "api_league_id": 94,
        "code": "PLP",
        "name": "Primera Liga",
        "country": "Portugal"
    },
    {
        "api_league_id": 88,
        "code": "ED",
        "name": "Eredivisie",
        "country": "Netherlands"
    }
]

for comp in competitions:

    existing = session.query(Competition).filter_by(
        api_league_id=comp["api_league_id"]
    ).first()

    if existing:
        continue

    new_comp = Competition(
        api_league_id=comp["api_league_id"],
        code=comp["code"],
        name=comp["name"],
        country=comp["country"]
    )

    session.add(new_comp)

session.commit()

print("Competitions seeded correctly")