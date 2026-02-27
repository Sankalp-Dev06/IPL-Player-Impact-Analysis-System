import streamlit as st
from theme import load_theme
import pandas as pd
import plotly.express as px
from queries import load_venue_intelligence

load_theme()

st.title("🏟 Venue Intelligence")

venue_df = load_venue_intelligence()

# Season filter
seasons = sorted(venue_df["season"].unique(), reverse=True)
selected_season = st.selectbox("Select Season", seasons)

season_df = venue_df[venue_df["season"] == selected_season]

st.subheader("Venue Ranking by Batting Index")

ranked_df = season_df.sort_values(
    "batting_to_wicket_ratio",
    ascending=False
).reset_index(drop=True)

ranked_df.index += 1

st.dataframe(
    ranked_df[[
        "venue_name",
        "avg_runs_per_match",
        "avg_wickets_per_match",
        "batting_to_wicket_ratio"
    ]],
    use_container_width=True
)

st.subheader("Runs vs Wickets Landscape")

fig = px.scatter(
    season_df,
    x="avg_runs_per_match",
    y="avg_wickets_per_match",
    size="total_matches",
    hover_name="venue_name",
    title="Venue Scoring Behavior"
)

fig.update_layout(
    xaxis_title="Average Runs Per Match",
    yaxis_title="Average Wickets Per Match"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Venue Classification")

classification_df = season_df.copy()

classification_df["venue_type"] = classification_df["batting_to_wicket_ratio"].apply(
    lambda x: "Batting Friendly" if x > 28
    else ("Bowling Friendly" if x < 22 else "Balanced")
)

classification_display = classification_df[[
    "venue_name",
    "batting_to_wicket_ratio",
    "venue_type"
]].sort_values("batting_to_wicket_ratio", ascending=False)

classification_display = classification_display.reset_index(drop=True)
classification_display.index += 1

st.table(classification_display)