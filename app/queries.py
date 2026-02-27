import pandas as pd

def load_player_overview():
    return pd.read_csv("data/player_overview.csv")

def load_player_form():
    df = pd.read_csv("data/player_form.csv")
    df["match_date"] = pd.to_datetime(df["match_date"])
    return df

def load_venue_intelligence():
    return pd.read_csv("data/venue_intelligence.csv")

def load_team_defense():
    return pd.read_csv("data/team_defense.csv")