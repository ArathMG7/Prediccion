from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, ForeignKey, func, UniqueConstraint

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

class Coach(Base):

    __tablename__ = "coaches"

    id = Column(
        Integer,
        primary_key=True
    )

    api_coach_id = Column(
        Integer,
        unique=True,
        nullable=False
    )

    name = Column(String)

    firstname = Column(String)

    lastname = Column(String)

    age = Column(Integer)

    nationality = Column(String)

    photo = Column(String)

class TeamCoach(Base):

    __tablename__ = "team_coaches"

    id = Column(
        Integer,
        primary_key=True
    )

    team_id = Column(
        Integer,
        ForeignKey("teams.id"),
        nullable=False
    )

    coach_id = Column(
        Integer,
        ForeignKey("coaches.id"),
        nullable=False
    )

    start_date = Column(DateTime)

    end_date = Column(DateTime)

class MatchContext(Base):
    __tablename__ = "match_context"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), unique=True, nullable=False)

    home_coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=True)
    away_coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=True)

    home_coach_tenure_days = Column(Integer, nullable=True)
    away_coach_tenure_days = Column(Integer, nullable=True)

    home_rest_days = Column(Integer, nullable=True)
    away_rest_days = Column(Integer, nullable=True)

    home_points = Column(Integer)

    away_points = Column(Integer)

    home_position = Column(Integer)

    away_position = Column(Integer)

    points_diff = Column(Integer)

    position_diff = Column(Integer)

    home_title_race = Column(Boolean)

    away_title_race = Column(Boolean)

    home_europe_race = Column(Boolean)

    away_europe_race = Column(Boolean)

    home_relegation_risk = Column(Boolean)

    away_relegation_risk = Column(Boolean)

class TeamPlayer(Base):
    __tablename__ = "team_players"

    id = Column(Integer, primary_key=True, autoincrement=True)

    team_id = Column(Integer, nullable=False, index=True)
    
    player_id = Column(Integer, nullable=False, index=True)

    player_name = Column(String, nullable=True)
    
    age = Column(Integer, nullable=True)
    
    shirt_number = Column(Integer, nullable=True)
    
    position = Column(String, nullable=True)
    
    season = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "player_id",
            "season",
            name="uq_team_players_team_player_season"
        ),
    )


class MatchLineup(Base):
    __tablename__ = "match_lineups"

    id = Column(Integer, primary_key=True, autoincrement=True)

    fixture_id = Column(Integer, nullable=False, index=True)
    
    match_id = Column(Integer, nullable=True, index=True)
    
    team_id = Column(Integer, nullable=False, index=True)
    
    coach_id = Column(Integer, nullable=True, index=True)

    formation = Column(String, nullable=True)

    player_id = Column(Integer, nullable=False, index=True)
    
    player_name = Column(String, nullable=True)
    
    shirt_number = Column(Integer, nullable=True)
    
    position = Column(String, nullable=True)  
    
    grid_position = Column(String, nullable=True)

    is_starter = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "fixture_id",
            "team_id",
            "player_id",
            "is_starter",
            name="uq_match_lineups_fixture_team_player_starter"
        ),
    )  

class MatchOdds(Base):
    __tablename__ = "match_odds"

    id = Column(Integer, primary_key=True)

    fixture_id = Column(Integer, nullable=False, index=True)

    bookmaker = Column(String)

    home_odd = Column(Float)
    draw_odd = Column(Float)
    away_odd = Column(Float)

    over_25 = Column(Float)
    under_25 = Column(Float)

    created_at = Column(DateTime)