from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_

from database.db import engine
from database.models import Match, MatchContext, TeamCoach, Competition

Session = sessionmaker(bind=engine)
session = Session()

ALLOWED_COMPETITIONS = [
    #"Premier League",
    #"La Liga",
    #"Serie A",
    #"Bundesliga",
    #"Ligue 1",
    "Eredivisie",
    "Primera Liga"
]

def get_active_coach_relation(team_id, match_date):
    return (
        session.query(TeamCoach)
        .filter(TeamCoach.team_id == team_id)
        .filter(TeamCoach.start_date <= match_date)
        .filter(
            or_(
                TeamCoach.end_date.is_(None),
                TeamCoach.end_date >= match_date
            )
        )
        .order_by(TeamCoach.start_date.desc())
        .first()
    )

def ensure_team(table, team_id):
    if team_id not in table:
        table[team_id] = {
            "points": 0,
            "gf": 0,
            "ga": 0,
            "played": 0
        }

def build_ranking(table):
    rows = []

    for team_id, stats in table.items():
        goal_diff = stats["gf"] - stats["ga"]
        rows.append((
            team_id,
            stats["points"],
            goal_diff,
            stats["gf"]
        ))

    rows.sort(
        key=lambda x: (
            x[1],   # points
            x[2],   # goal diff
            x[3],   # goals for
            -x[0]   # stable tie-break
        ),
        reverse=True
    )

    return {
        team_id: idx + 1
        for idx, (team_id, _, _, _) in enumerate(rows)
    }

matches = (
    session.query(Match)
    .join(Competition, Match.competition_id == Competition.id)
    .filter(Competition.name.in_(ALLOWED_COMPETITIONS))
    .filter(Match.status.in_(["FT", "AET", "PEN"]))
    .order_by(
        Competition.id.asc(),
        Match.season.asc(),
        Match.date.asc(),
        Match.id.asc()
    )
    .all()
)

# Group by competition + season
matches_by_key = defaultdict(list)
for match in matches:
    matches_by_key[(match.competition_id, match.season)].append(match)

counter = 0
total_matches = len(matches)

print(f"Total matches: {total_matches}")

for (competition_id, season), season_matches in matches_by_key.items():

    # Seed all teams in this competition-season with zeroed standings
    team_ids = set()
    for match in season_matches:
        team_ids.add(match.home_team_id)
        team_ids.add(match.away_team_id)

    standings = {
        team_id: {
            "points": 0,
            "gf": 0,
            "ga": 0,
            "played": 0
        }
        for team_id in team_ids
    }

    season_matches = sorted(
        season_matches,
        key=lambda m: (m.date, m.id)
    )

    for match in season_matches:
        counter += 1

        try:
            home_team_id = match.home_team_id
            away_team_id = match.away_team_id

            ensure_team(standings, home_team_id)
            ensure_team(standings, away_team_id)

            ranking = build_ranking(standings)

            home_points = standings[home_team_id]["points"]
            away_points = standings[away_team_id]["points"]

            home_position = ranking[home_team_id]
            away_position = ranking[away_team_id]

            total_teams = len(standings)
            relegation_cutoff = max(total_teams - 2, 1)

            home_rel = get_active_coach_relation(
                home_team_id,
                match.date
            )
            away_rel = get_active_coach_relation(
                away_team_id,
                match.date
            )

            existing_context = (
                session.query(MatchContext)
                .filter_by(match_id=match.id)
                .first()
            )

            if not existing_context:
                existing_context = MatchContext(match_id=match.id)
                session.add(existing_context)

            # Coaches
            existing_context.home_coach_id = (
                home_rel.coach_id if home_rel else None
            )
            existing_context.away_coach_id = (
                away_rel.coach_id if away_rel else None
            )

            existing_context.home_coach_tenure_days = (
                (match.date.date() - home_rel.start_date.date()).days
                if home_rel and home_rel.start_date else None
            )
            existing_context.away_coach_tenure_days = (
                (match.date.date() - away_rel.start_date.date()).days
                if away_rel and away_rel.start_date else None
            )

            # Points / standings before the match
            existing_context.home_points = home_points
            existing_context.away_points = away_points

            existing_context.home_position = home_position
            existing_context.away_position = away_position

            existing_context.points_diff = home_points - away_points
            existing_context.position_diff = away_position - home_position

            # Simple competition flags
            existing_context.home_title_race = home_position <= 3
            existing_context.away_title_race = away_position <= 3

            existing_context.home_europe_race = home_position <= 6
            existing_context.away_europe_race = away_position <= 6

            existing_context.home_relegation_risk = (
                home_position >= relegation_cutoff
            )
            existing_context.away_relegation_risk = (
                away_position >= relegation_cutoff
            )

            # Update standings AFTER storing pre-match context
            home_goals = int(match.home_goals or 0)
            away_goals = int(match.away_goals or 0)

            standings[home_team_id]["played"] += 1
            standings[away_team_id]["played"] += 1

            standings[home_team_id]["gf"] += home_goals
            standings[home_team_id]["ga"] += away_goals

            standings[away_team_id]["gf"] += away_goals
            standings[away_team_id]["ga"] += home_goals

            if home_goals > away_goals:
                standings[home_team_id]["points"] += 3
            elif home_goals < away_goals:
                standings[away_team_id]["points"] += 3
            else:
                standings[home_team_id]["points"] += 1
                standings[away_team_id]["points"] += 1

            if counter % 100 == 0:
                session.commit()
                print(f"Committed {counter}/{total_matches}")

        except Exception as e:
            session.rollback()
            print(f"Error in match {match.id} ({match.api_fixture_id})")
            print(e)

session.commit()
print("Completed")