import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data/raw/premier_league_matches.csv")

engine = create_engine("sqlite:///data/soccer.db")

df.to_sql(
    "matches",
    con=engine,
    if_exists="replace",
    index=False
)

print("Datos guardados en SQLite")