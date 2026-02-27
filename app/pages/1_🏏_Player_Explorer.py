import streamlit as st
import pandas as pd
import plotly.express as px
from queries import load_player_overview, load_player_form

st.title("🏏 Player Explorer")

# Load data
overview_df = load_player_overview()
form_df = load_player_form()

# Season selector
seasons = sorted(overview_df["season"].unique(), reverse=True)
selected_season = st.selectbox("Select Season", seasons)

# Filter by season
season_df = overview_df[overview_df["season"] == selected_season]

# Player selector
players = sorted(season_df["player_name"].unique())
selected_player = st.selectbox("Select Player", players)

player_stats = season_df[season_df["player_name"] == selected_player]

if not player_stats.empty:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Average Impact", round(player_stats["avg_impact"].values[0], 2))
    col2.metric("Matches Played", int(player_stats["total_matches"].values[0]))
    col3.metric("Consistency (CV)", round(player_stats["coefficient_of_variation"].values[0], 2))
    col4.metric("Role", player_stats["player_role"].values[0])

    cv = player_stats["coefficient_of_variation"].values[0]

    if cv < 0.6:
        stability_label = "Highly Consistent"
    elif cv < 1.0:
        stability_label = "Moderately Stable"
    else:
        stability_label = "Highly Volatile"

    st.info(f"Performance Profile: **{stability_label}**")

player_form = form_df[
    (form_df["player_name"] == selected_player) &
    (form_df["season"] == selected_season)
]

if not player_form.empty:
    st.subheader("Impact Distribution")

    fig_hist = px.histogram(
        player_form,
        x="impact_score",
        nbins=15,
        opacity=0.8
    )

    fig_hist.update_layout(
        showlegend=False,
        xaxis_title="Impact Score",
        yaxis_title="Match Count"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Form Trend")

    player_form = player_form.sort_values("match_date")

    fig_line = px.line(
        player_form,
        x="match_date",
        y="impact_score",
        markers=True,
        hover_data=["opponent_team", "venue_name"]
    )

    fig_line.add_scatter(
        x=player_form["match_date"],
        y=player_form["rolling_5_match_impact"],
        mode="lines",
        name="Rolling 5-Match Form"
    )

    fig_line.update_layout(
        xaxis_title="Match Date",
        yaxis_title="Impact Score",
        legend_title="Metrics"
    )

    st.plotly_chart(fig_line, use_container_width=True)