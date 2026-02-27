WITH Batting AS (
    SELECT
        batter_id AS player_id,
        match_id,
        batting_team_id AS team_id,
        SUM(runs_batter) AS runs,
        COUNT(CASE WHEN wides = 0 THEN 1 END) AS balls_faced,
        SUM(CASE WHEN runs_batter = 4 THEN 1 ELSE 0 END) AS fours,
        SUM(CASE WHEN runs_batter = 6 THEN 1 ELSE 0 END) AS sixes
    FROM Deliveries
    GROUP BY batter_id, match_id, batting_team_id
),

Bowling AS (
    SELECT
        bowler_id AS player_id,
        d.match_id,
        CASE
            WHEN d.batting_team_id = m.team1_id THEN m.team2_id
            ELSE m.team1_id
        END AS team_id,
        SUM(CASE WHEN is_wicket = 1 THEN 1 ELSE 0 END) AS wickets,
        COUNT(CASE WHEN wides = 0 AND noballs = 0 THEN 1 END) AS legal_balls,
        SUM(total_runs) AS runs_conceded
    FROM Deliveries d
    JOIN Matches m ON d.match_id = m.match_id
    GROUP BY bowler_id, d.match_id,
        CASE
            WHEN d.batting_team_id = m.team1_id THEN m.team2_id
            ELSE m.team1_id
        END
),

Fielding AS (
    SELECT
        fielder_id AS player_id,
        match_id,
        batting_team_id AS team_id,
        COUNT(*) AS catches
    FROM Deliveries
    WHERE dismissal_type = 'caught'
    GROUP BY fielder_id, match_id, batting_team_id
)

INSERT INTO Player_Match_Summary
SELECT
    COALESCE(b.player_id, bw.player_id, f.player_id) AS player_id,
    COALESCE(b.match_id, bw.match_id, f.match_id) AS match_id,
    COALESCE(b.team_id, bw.team_id, f.team_id) AS team_id,

    ISNULL(b.runs, 0),
    ISNULL(b.balls_faced, 0),
    ISNULL(b.fours, 0),
    ISNULL(b.sixes, 0),

    CASE WHEN ISNULL(b.balls_faced, 0) > 0
         THEN b.runs * 100.0 / b.balls_faced
         ELSE 0 END,

    ISNULL(bw.wickets, 0),
    ISNULL(bw.legal_balls, 0),
    ISNULL(bw.runs_conceded, 0),

    CASE WHEN ISNULL(bw.legal_balls, 0) > 0
         THEN bw.runs_conceded * 6.0 / bw.legal_balls
         ELSE 0 END,

    ISNULL(f.catches, 0)

FROM Batting b
FULL OUTER JOIN Bowling bw
    ON b.player_id = bw.player_id AND b.match_id = bw.match_id
FULL OUTER JOIN Fielding f
    ON COALESCE(b.player_id, bw.player_id) = f.player_id
    AND COALESCE(b.match_id, bw.match_id) = f.match_id;

SELECT COUNT(*) AS total_rows 
FROM Player_Match_Summary;

SELECT COUNT(*) 
FROM Player_Match_Summary p
LEFT JOIN Players pl ON p.player_id = pl.player_id
WHERE pl.player_id IS NULL;

SELECT COUNT(*) 
FROM Player_Match_Summary p
LEFT JOIN Teams t ON p.team_id = t.team_id
WHERE t.team_id IS NULL;

SELECT * 
FROM Player_Match_Summary
WHERE match_id = 1216524;

SELECT 
    MIN(strike_rate) AS min_sr,
    MAX(strike_rate) AS max_sr,
    MIN(economy) AS min_eco,
    MAX(economy) AS max_eco
FROM Player_Match_Summary;