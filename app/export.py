import pandas as pd
from db import get_connection

conn = get_connection()

views = {
    "player_overview": "SELECT * FROM vw_Player_Overview_Season",
    "player_form": "SELECT * FROM vw_Player_Form_Display",
    "venue_intelligence": "SELECT * FROM vw_Venue_Intelligence",
    "team_defense": "SELECT * FROM vw_Team_Defensive_Strength"
}

for name, query in views.items():
    df = pd.read_sql(query, conn)
    df.to_csv(f"app/data/{name}.csv", index=False)

conn.close()

print("Export completed.")