import streamlit as st
from theme import load_theme
import pandas as pd
import plotly.express as px
from queries import load_team_defense

load_theme()

st.title("🛡 Team Defensive Strength")

defense_df = load_team_defense()

# Season filter
seasons = sorted(defense_df["season"].unique(), reverse=True)
selected_season = st.selectbox("Select Season", seasons)

season_df = defense_df[defense_df["season"] == selected_season]

st.subheader("Defensive Ranking (Lower Impact Conceded = Stronger)")

ranked_df = season_df.sort_values(
    "avg_impact_conceded",
    ascending=True
).reset_index(drop=True)

ranked_df.index += 1

st.dataframe(
    ranked_df[[
        "team_name",
        "avg_impact_conceded",
        "total_matches"
    ]],
    use_container_width=True
)

st.subheader("Impact Conceded by Team")

fig = px.bar(
    ranked_df,
    x="team_name",
    y="avg_impact_conceded",
    title="Average Impact Conceded per Match",
)

fig.update_layout(
    xaxis_title="Team",
    yaxis_title="Avg Impact Conceded"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Defensive Tier Classification")

classification_df = ranked_df.copy()

classification_df["defensive_tier"] = classification_df["avg_impact_conceded"].apply(
    lambda x: "Elite Defense" if x < 280
    else ("Weak Defense" if x > 320 else "Average Defense")
)

classification_display = classification_df[[
    "team_name",
    "avg_impact_conceded",
    "defensive_tier"
]]

st.table(classification_display)