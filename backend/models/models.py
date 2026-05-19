from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey

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
    round = Column(String)

    home_team_id = Column(Integer)
    away_team_id = Column(Integer)

    home_goals = Column(Integer)
    away_goals = Column(Integer)

    status = Column(String)

    referee = Column(String)

class MatchStatistics(Base):

    __tablename__ = "match_statistics"

    id = Column(Integer, primary_key=True)

    match_id = Column(
        Integer,
        ForeignKey("matches.id")
    )

    home_shots = Column(Integer)
    away_shots = Column(Integer)

    home_shots_on_target = Column(Integer)
    away_shots_on_target = Column(Integer)

    home_possession = Column(Float)
    away_possession = Column(Float)

    home_corners = Column(Integer)
    away_corners = Column(Integer)

    home_fouls = Column(Integer)
    away_fouls = Column(Integer)

    home_yellow_cards = Column(Integer)
    away_yellow_cards = Column(Integer)

    home_red_cards = Column(Integer)
    away_red_cards = Column(Integer)

    home_xg = Column(Float)
    away_xg = Column(Float)