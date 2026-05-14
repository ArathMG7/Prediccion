from services.api_football_service import (
    get_teams_by_league_and_season
)

teams = get_teams_by_league_and_season(
    39,
    2024
)

print(f"Total teams: {len(teams)}")

for team in teams[:5]:

    print(team["team"]["name"])