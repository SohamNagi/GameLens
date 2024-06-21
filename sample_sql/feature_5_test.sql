SELECT
    m.id,
    m.season,

    m.home_team_goal as home_team_goals,
    t1.team_long_name as home_team_name,

    m.away_team_goal as away_team_goals,
    t2.team_long_name as away_team_name
FROM
    match m
INNER JOIN
    team t1 ON m.home_team_api_id = t1.team_api_id
INNER JOIN
    team t2 ON m.away_team_api_id = t2.team_api_id
WHERE m.id = 22005;
