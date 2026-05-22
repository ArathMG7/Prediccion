from sqlalchemy.orm import sessionmaker

from database.db import engine

from database.models import (
    Match,
    MatchStatistics
)

from services.api_football_service import (
    get_match_statistics
)

import time

Session = sessionmaker(bind=engine)

session = Session()

matches = (
    session.query(Match)
    .outerjoin(
        MatchStatistics,
        Match.id == MatchStatistics.match_id
    )
    .filter(
        MatchStatistics.id == None
    )
    .filter(
        Match.status.in_([
            "FT",
            "AET",
            "PEN"
        ])
    )
    .all()
)

counter = 0

total_matches = len(matches)

print(
    f"Total matches: {total_matches}"
)

for match in matches:

    try:

        print(
            f"[{counter}/{total_matches}] "
            f"Fetching {match.api_fixture_id}"
        )

        stats = get_match_statistics(
            match.api_fixture_id
        )

        if len(stats) < 2:
            continue
        
        home_stats = stats[0]["statistics"]
        away_stats = stats[1]["statistics"]

        def get_stat(
            stats_list,
            stat_name
        ):

            for stat in stats_list:

                if stat["type"] == stat_name:
                    value = stat["value"]

                    if value is None:
                        return None

                    if isinstance(value, str):

                        value = value.replace("%", "")

                    return value

            return None

        home_possession = get_stat(
            home_stats,
            "Ball Possession"
        )

        away_possession = get_stat(
            away_stats,
            "Ball Possession"
        )

        new_stats = MatchStatistics(

            match_id=match.id,

            home_shots=
                get_stat(
                    home_stats,
                    "Total Shots"
                ),

            away_shots=
                get_stat(
                    away_stats,
                    "Total Shots"
                ),

            home_shots_on_target=
                get_stat(
                    home_stats,
                    "Shots on Goal"
                ),

            away_shots_on_target=
                get_stat(
                    away_stats,
                    "Shots on Goal"
                ),

            home_possession=
                float(home_possession)
                if home_possession
                else None,

            away_possession=
                float(away_possession)
                if away_possession
                else None,

            home_corners=
                get_stat(
                    home_stats,
                    "Corner Kicks"
                ),

            away_corners=
                get_stat(
                    away_stats,
                    "Corner Kicks"
                ),

            home_fouls=
                get_stat(
                    home_stats,
                    "Fouls"
                ),

            away_fouls=
                get_stat(
                    away_stats,
                    "Fouls"
                ),

            home_yellow_cards=
                get_stat(
                    home_stats,
                    "Yellow Cards"
                ),

            away_yellow_cards=
                get_stat(
                    away_stats,
                    "Yellow Cards"
                ),

            home_red_cards=
                get_stat(
                    home_stats,
                    "Red Cards"
                ),

            away_red_cards=
                get_stat(
                    away_stats,
                    "Red Cards"
                )
        )

        session.add(new_stats)
        counter += 1

        if counter % 25 == 0:

            session.commit()

            print(
                f"Committed {counter}"
            )

        print(
            f"Saved stats for {match.api_fixture_id}"
        )

        time.sleep(1)

    except Exception as e:
        
        session.rollback()
        print(
            f"Error {match.api_fixture_id}"
        )
        
        print(e)

session.commit()