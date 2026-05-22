from sqlalchemy.orm import sessionmaker

from database.db import engine

from database.models import (
    Team,
    Coach,
    TeamCoach
)

from services.api_football_service import (
    get_coaches_by_team
)

from datetime import datetime

import time

Session = sessionmaker(bind=engine)

session = Session()

teams = session.query(Team).all()

counter = 0

total_teams = len(teams)

print(
    f"Teams: {total_teams}"
)

for team in teams:

    try:

        print(
            f"[{counter}/{total_teams}] "
            f"{team.name}"
        )

        coaches = get_coaches_by_team(
            team.api_team_id
        )
        for coach_data in coaches:

            coach_info = coach_data

            existing_coach = session.query(
                Coach
            ).filter_by(
                api_coach_id=coach_info["id"]
            ).first()
            
            if not existing_coach:

                age = coach_info.get("age")

                if age:
                    try:
                        age = int(age)
                    except:
                        age = None

                new_coach = Coach(

                    api_coach_id=
                        coach_info["id"],

                    name=
                        coach_info.get("name"),

                    firstname=
                        coach_info.get("firstname"),

                    lastname=
                        coach_info.get("lastname"),

                    age=age,

                    nationality=
                        coach_info.get(
                            "nationality"
                        ),

                    photo=
                        coach_info.get("photo")
                )

                session.add(new_coach)

                session.flush()

                coach_id = new_coach.id

            else:

                coach_id = existing_coach.id

            career = coach_data.get(
                "career",
                []
              )
            for job in career:

                if (
                    not job.get("team")
                    or not job["team"].get("id")
                ):
                    continue
                
                db_team = session.query(
                    Team
                ).filter_by(
                    api_team_id=
                        job["team"]["id"]
                ).first()

                if not db_team:
                    continue
                
                start_date = None
                end_date = None

                if job.get("start"):

                    try:

                        start_date = (
                            datetime.fromisoformat(
                                job["start"]
                                .replace(
                                    "Z",
                                    "+00:00"
                                )
                            )
                        )

                    except:
                        pass

                if job.get("end"):

                    try:

                        end_date = (
                            datetime.fromisoformat(
                                job["end"]
                                .replace(
                                    "Z",
                                    "+00:00"
                                )
                            )
                        )

                    except:
                        pass
                    
                existing_relation = (
                    session.query(
                        TeamCoach
                    ).filter_by(
                        team_id=db_team.id,
                        coach_id=coach_id,
                        start_date=start_date
                    ).first()
                )

                if existing_relation:
                    continue
                relation = TeamCoach(

                    team_id=db_team.id,

                    coach_id=coach_id,

                    start_date=start_date,

                    end_date=end_date
                )

                session.add(relation)
        
        counter += 1

        if counter % 10 == 0:

            session.commit()

            print(
                f"Committed {counter}"
            )

        time.sleep(2)
    except Exception as e:

        session.rollback()

        print(
            f"Error {team.name}"
        )

        print(e)

session.commit()

print("Completed")