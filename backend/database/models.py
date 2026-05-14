from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)

    api_team_id = Column(Integer, unique=True)

    name = Column(String)

    short_name = Column(String)

    code = Column(String)

    country = Column(String)

    founded = Column(Integer)

    logo = Column(String)

    venue_name = Column(String)

    venue_city = Column(String)

    venue_capacity = Column(Integer)

class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)

    api_league_id = Column(Integer, unique=True)

    code = Column(String)

    name = Column(String)

    country = Column(String)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)

    api_fixture_id = Column(Integer, unique=True)

    competition_id = Column(Integer)
    season = Column(Integer)

    date = Column(DateTime)

    home_team_id = Column(Integer)
    away_team_id = Column(Integer)

    home_goals = Column(Integer)
    away_goals = Column(Integer)

    status = Column(String)

    referee = Column(String)