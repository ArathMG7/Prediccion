import pandas as pd
from sqlalchemy import create_engine

from services.api_football_service import (
    get_team_squad
)

DB_PATH = "data/soccer.db"

SEASON = 2025

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

teams_df = pd.read_sql(
    """
    SELECT
        id
    FROM Teams
    """,
    engine
)

existing_df = pd.read_sql(
    """
    SELECT DISTINCT
        team_id,
        season
    FROM team_players
    """,
    engine
)

existing_keys = set(
    zip(
        existing_df["team_id"],
        existing_df["season"]
    )
)

pending_teams = []

for _, team in teams_df.iterrows():

    key = (
        int(team["id"]),
        SEASON
    )

    if key not in existing_keys:

        pending_teams.append(
            int(team["id"])
        )

print()
print(f"Teams totales: {len(teams_df)}")
print(f"Ya descargados: {len(existing_keys)}")
print(f"Pendientes: {len(pending_teams)}")
print()

success = 0
failed = 0

total = len(
    pending_teams
)

for idx, team_id in enumerate(
    pending_teams,
    start=1
):

    try:

        print(
            f"[{idx}/{total}] Team {team_id}"
        )

        squad_response = (
            get_team_squad(
                team_id
            )
        )

        if not squad_response:

            continue

        players = (
            squad_response[0]
            .get(
                "players",
                []
            )
        )

        with engine.begin() as conn:

            for player in players:

                conn.exec_driver_sql(
                    """
                    INSERT INTO team_players
                    (
                        team_id,
                        player_id,
                        player_name,
                        age,
                        shirt_number,
                        position,
                        season
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        team_id,

                        player.get("id"),

                        player.get("name"),

                        player.get("age"),

                        player.get("number"),

                        player.get("position"),

                        SEASON
                    )
                )

        success += 1

    except Exception as ex:

        failed += 1

        print(
            f"ERROR Team {team_id}: {ex}"
        )

print()
print(f"SUCCESS: {success}")
print(f"FAILED: {failed}")