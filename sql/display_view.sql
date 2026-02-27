CREATE OR ALTER VIEW vw_Player_Overview_Season AS
SELECT
    p.player_id,
    pl.player_name,
    m.season,

    COUNT(*) AS total_matches,

    AVG(p.impact_score) AS avg_impact,

    STDEV(p.impact_score) AS std_impact,

    CASE 
        WHEN AVG(p.impact_score) = 0 THEN NULL
        ELSE STDEV(p.impact_score) / AVG(p.impact_score)
    END AS coefficient_of_variation,

    AVG(p.balls_faced) AS avg_balls_faced,
    AVG(p.legal_balls) AS avg_legal_balls,

    CASE
        WHEN AVG(p.balls_faced) >= 15 AND AVG(p.legal_balls) < 6 THEN 'Batsman'
        WHEN AVG(p.legal_balls) >= 12 AND AVG(p.balls_faced) < 10 THEN 'Bowler'
        WHEN AVG(p.balls_faced) >= 10 AND AVG(p.legal_balls) >= 6 THEN 'All-Rounder'
        ELSE 'Utility'
    END AS player_role

FROM Player_Match_Summary p
JOIN Matches m ON p.match_id = m.match_id
JOIN Players pl ON p.player_id = pl.player_id

GROUP BY
    p.player_id,
    pl.player_name,
    m.season

HAVING COUNT(*) >= 8;  -- minimum matches per season

CREATE OR ALTER VIEW vw_Player_Form_Display AS
WITH Base AS (
    SELECT
        p.player_id,
        pl.player_name,
        m.match_id,
        m.season,
        m.match_date,
        m.venue_id,
        v.venue_name,
        p.team_id,
        p.impact_score,

        CASE
            WHEN p.team_id = m.team1_id THEN m.team2_id
            ELSE m.team1_id
        END AS opponent_team_id

    FROM Player_Match_Summary p
    JOIN Matches m ON p.match_id = m.match_id
    JOIN Players pl ON p.player_id = pl.player_id
    JOIN Venues v ON m.venue_id = v.venue_id
)

SELECT
    b.player_id,
    b.player_name,
    b.season,
    b.match_date,
    b.impact_score,

    AVG(b.impact_score) OVER (
        PARTITION BY b.player_id
        ORDER BY b.match_date
        ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING
    ) AS rolling_5_match_impact,

    b.venue_name,
    t.team_name AS opponent_team

FROM Base b
LEFT JOIN Teams t ON b.opponent_team_id = t.team_id;

CREATE OR ALTER VIEW vw_Venue_Intelligence AS
WITH Match_Aggregate AS (
    SELECT
        m.match_id,
        m.season,
        m.venue_id,
        v.venue_name,

        SUM(p.runs) AS total_runs_in_match,
        SUM(p.wickets) AS total_wickets_in_match

    FROM Player_Match_Summary p
    JOIN Matches m ON p.match_id = m.match_id
    JOIN Venues v ON m.venue_id = v.venue_id

    GROUP BY
        m.match_id,
        m.season,
        m.venue_id,
        v.venue_name
)

SELECT
    season,
    venue_id,
    venue_name,

    COUNT(match_id) AS total_matches,

    AVG(total_runs_in_match) AS avg_runs_per_match,
    AVG(total_wickets_in_match) AS avg_wickets_per_match,

    CASE
        WHEN AVG(total_wickets_in_match) = 0 THEN NULL
        ELSE AVG(total_runs_in_match) * 1.0 /
             AVG(total_wickets_in_match)
    END AS batting_to_wicket_ratio

FROM Match_Aggregate
GROUP BY
    season,
    venue_id,
    venue_name

HAVING COUNT(match_id) >= 5;


CREATE OR ALTER VIEW vw_Team_Defensive_Strength AS
WITH Match_Defense AS (
    SELECT
        m.match_id,
        m.season,

        -- Team 1 conceded impact from Team 2 players
        m.team1_id AS defending_team_id,
        SUM(CASE WHEN p.team_id = m.team2_id THEN p.impact_score ELSE 0 END)
            AS impact_conceded

    FROM Matches m
    JOIN Player_Match_Summary p ON m.match_id = p.match_id
    GROUP BY m.match_id, m.season, m.team1_id

    UNION ALL

    SELECT
        m.match_id,
        m.season,

        -- Team 2 conceded impact from Team 1 players
        m.team2_id AS defending_team_id,
        SUM(CASE WHEN p.team_id = m.team1_id THEN p.impact_score ELSE 0 END)
            AS impact_conceded

    FROM Matches m
    JOIN Player_Match_Summary p ON m.match_id = p.match_id
    GROUP BY m.match_id, m.season, m.team2_id
)

SELECT
    md.season,
    md.defending_team_id AS team_id,
    t.team_name,

    COUNT(md.match_id) AS total_matches,

    AVG(md.impact_conceded) AS avg_impact_conceded

FROM Match_Defense md
JOIN Teams t ON md.defending_team_id = t.team_id

GROUP BY
    md.season,
    md.defending_team_id,
    t.team_name

HAVING COUNT(md.match_id) >= 8;