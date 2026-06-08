import pandas as pd
from sqlalchemy import create_engine

from services.api_football_service import (
    get_fixture_lineups
)

DB_PATH = "data/soccer.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

matches_df = pd.read_sql(
    """
    SELECT
        id,
        api_fixture_id,
        season
    FROM matches
    WHERE api_fixture_id IS NOT NULL
    """,
    engine
)

existing_df = pd.read_sql(
    """
    SELECT DISTINCT
        fixture_id
    FROM match_lineups
    """,
    engine
)

existing_fixtures = set(
    existing_df["fixture_id"]
)

pending_matches = matches_df[
    ~matches_df["api_fixture_id"]
    .isin(
        existing_fixtures
    )
].copy()

print()
print(
    f"Fixtures totales: {len(matches_df)}"
)

print(
    f"Ya descargados: {len(existing_fixtures)}"
)

print(
    f"Pendientes: {len(pending_matches)}"
)

print()

success = 0
failed = 0

total = len(
    pending_matches
)

for idx, (_, match) in enumerate(
    pending_matches.iterrows(),
    start=1
):

    match_id = int(
        match["id"]
    )

    fixture_id = int(
        match["api_fixture_id"]
    )

    try:

        print(
            f"[{idx}/{total}] Fixture {fixture_id}"
        )

        lineups = (
            get_fixture_lineups(
                fixture_id
            )
        )

        if not lineups:

            continue

        with engine.begin() as conn:

            for lineup in lineups:

                team_id = (
                    lineup["team"]["id"]
                )

                coach = (
                    lineup.get(
                        "coach"
                    )
                    or {}
                )

                coach_id = (
                    coach.get("id")
                )

                formation = (
                    lineup.get(
                        "formation"
                    )
                )

                # TITULARES

                for starter in lineup.get(
                    "startXI",
                    []
                ):

                    player = (
                        starter["player"]
                    )

                    conn.exec_driver_sql(
                        """
                        INSERT INTO match_lineups
                        (
                            fixture_id,
                            match_id,
                            team_id,
                            coach_id,
                            formation,
                            player_id,
                            player_name,
                            shirt_number,
                            position,
                            grid_position,
                            is_starter
                        )
                        VALUES
                        (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (
                            fixture_id,
                            match_id,
                            team_id,
                            coach_id,
                            formation,

                            player.get("id"),

                            player.get("name"),

                            player.get("number"),

                            player.get("pos"),

                            player.get("grid"),

                            1
                        )
                    )

                # SUPLENTES

                for substitute in lineup.get(
                    "substitutes",
                    []
                ):

                    player = (
                        substitute["player"]
                    )

                    conn.exec_driver_sql(
                        """
                        INSERT INTO match_lineups
                        (
                            fixture_id,
                            match_id,
                            team_id,
                            coach_id,
                            formation,
                            player_id,
                            player_name,
                            shirt_number,
                            position,
                            grid_position,
                            is_starter
                        )
                        VALUES
                        (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        (
                            fixture_id,
                            match_id,
                            team_id,
                            coach_id,
                            formation,

                            player.get("id"),

                            player.get("name"),

                            player.get("number"),

                            player.get("pos"),

                            None,

                            0
                        )
                    )

        success += 1

    except Exception as ex:

        failed += 1

        print(
            f"ERROR Fixture {fixture_id}: {ex}"
        )

print()
print(f"SUCCESS: {success}")
print(f"FAILED: {failed}")