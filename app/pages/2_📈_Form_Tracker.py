import streamlit as st
from theme import load_theme
import pandas as pd
import plotly.express as px
from queries import load_player_form

load_theme()

st.title("📈 League Form Tracker")

form_df = load_player_form()

# Season filter
seasons = sorted(form_df["season"].unique(), reverse=True)
selected_season = st.selectbox("Select Season", seasons)

season_df = form_df[form_df["season"] == selected_season]

# Get latest rolling form per player
latest_form = (
    season_df
    .sort_values("match_date")
    .groupby("player_name")
    .tail(1)
)

latest_form = latest_form.sort_values(
    "rolling_5_match_impact",
    ascending=False
)

st.subheader("Top 10 In-Form Players")

top10 = latest_form.head(10)[
    ["player_name", "rolling_5_match_impact"]
]

top10_display = top10.reset_index(drop=True)
top10_display.index = top10_display.index + 1

st.dataframe(top10_display)

st.subheader("Top 5 Form Trend")

top5_players = top10["player_name"].head(5).tolist()

top5_df = season_df[
    season_df["player_name"].isin(top5_players)
]

fig = px.line(
    top5_df,
    x="match_date",
    y="rolling_5_match_impact",
    color="player_name",
    markers=True
)

fig.update_layout(
    xaxis_title="Match Date",
    yaxis_title="Rolling 5-Match Impact",
    legend_title="Player"
)

st.plotly_chart(fig, use_container_width=True)