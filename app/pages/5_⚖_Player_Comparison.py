import streamlit as st
from theme import load_theme
import pandas as pd
import plotly.express as px
from queries import load_player_overview, load_player_form

load_theme()

st.title("⚖ Player Comparison")

overview_df = load_player_overview()
form_df = load_player_form()

# Season selection
seasons = sorted(overview_df["season"].unique(), reverse=True)
selected_season = st.selectbox("Select Season", seasons)

season_overview = overview_df[overview_df["season"] == selected_season]
season_form = form_df[form_df["season"] == selected_season]

players = sorted(season_overview["player_name"].unique())

col1, col2 = st.columns(2)

player1 = col1.selectbox("Select Player 1", players, key="p1")
player2 = col2.selectbox("Select Player 2", players, key="p2")

if player1 != player2:

    stats1 = season_overview[season_overview["player_name"] == player1]
    stats2 = season_overview[season_overview["player_name"] == player2]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(player1)
        st.metric("Avg Impact", round(stats1["avg_impact"].values[0], 2))
        st.metric("Consistency (CV)", round(stats1["coefficient_of_variation"].values[0], 2))
        st.metric("Role", stats1["player_role"].values[0])

    with col2:
        st.subheader(player2)
        st.metric("Avg Impact", round(stats2["avg_impact"].values[0], 2))
        st.metric("Consistency (CV)", round(stats2["coefficient_of_variation"].values[0], 2))
        st.metric("Role", stats2["player_role"].values[0])
        

st.subheader("Impact Distribution Comparison")

p1_form = season_form[season_form["player_name"] == player1]
p2_form = season_form[season_form["player_name"] == player2]

combined_df = pd.concat([
    p1_form.assign(player=player1),
    p2_form.assign(player=player2)
])

fig_hist = px.histogram(
    combined_df,
    x="impact_score",
    color="player",
    barmode="overlay",
    opacity=0.6
)

st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Rolling Form Comparison")

combined_trend = pd.concat([
    p1_form.assign(player=player1),
    p2_form.assign(player=player2)
])

fig_line = px.line(
    combined_trend,
    x="match_date",
    y="rolling_5_match_impact",
    color="player",
    markers=True
)

st.plotly_chart(fig_line, use_container_width=True)