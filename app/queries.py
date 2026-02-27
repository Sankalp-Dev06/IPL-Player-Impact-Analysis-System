import pandas as pd
from db import get_connection

def load_player_overview():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM vw_Player_Overview_Season", conn)
    conn.close()
    return df

def load_player_form():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM vw_Player_Form_Display", conn)
    conn.close()
    return df

def load_venue_intelligence():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM vw_Venue_Intelligence", conn)
    conn.close()
    return df

def load_team_defense():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM vw_Team_Defensive_Strength", conn)
    conn.close()
    return df