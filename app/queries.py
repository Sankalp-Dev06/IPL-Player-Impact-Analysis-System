import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)

def load_player_overview():
    return pd.read_csv(os.path.join(BASE_DIR, "data", "player_overview.csv"))

def load_player_form():
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "player_form.csv"))
    df["match_date"] = pd.to_datetime(df["match_date"])
    return df

def load_venue_intelligence():
    return pd.read_csv(os.path.join(BASE_DIR, "data", "venue_intelligence.csv"))

def load_team_defense():
    return pd.read_csv(os.path.join(BASE_DIR, "data", "team_defense.csv"))