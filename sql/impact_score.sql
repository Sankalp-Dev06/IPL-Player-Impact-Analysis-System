ALTER TABLE Player_Match_Summary
ADD impact_score FLOAT;

UPDATE Player_Match_Summary
SET impact_score =

    -- Batting base
    runs
    + 0.5 * fours
    + 1.0 * sixes

    -- Strike rate adjustment
    + CASE
        WHEN balls_faced >= 10
        THEN (strike_rate - 130) * 0.1
        ELSE 0
      END

    -- Bowling base
    + wickets * 25

    -- Economy adjustment
    + CASE
        WHEN legal_balls >= 12
        THEN (7.5 - economy) * 2
        ELSE 0
      END

    -- Fielding
    + catches * 8;

SELECT 
    MIN(impact_score) AS min_impact,
    MAX(impact_score) AS max_impact,
    AVG(impact_score) AS avg_impact
FROM Player_Match_Summary;

SELECT TOP 20 *
FROM Player_Match_Summary
ORDER BY impact_score DESC;

select * from Players
where player_id = 85


CREATE VIEW vw_Player_Form AS
SELECT
    p.player_id,
    p.match_id,
    m.match_date,
    p.impact_score,

    AVG(p.impact_score) OVER (
        PARTITION BY p.player_id
        ORDER BY m.match_date
        ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING
    ) AS rolling_5_match_impact

FROM Player_Match_Summary p
JOIN Matches m ON p.match_id = m.match_id;

SELECT TOP 20 *
FROM vw_Player_Form
ORDER BY rolling_5_match_impact DESC;