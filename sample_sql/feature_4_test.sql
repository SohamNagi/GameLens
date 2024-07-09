SELECT
  Player.player_name,
  pa.overall_rating
FROM
  Player
  JOIN Player_Attributes pa ON Player.player_api_id = pa.player_api_id
WHERE
  Player.id = 1323
  AND pa.date = (
    SELECT
      MAX(pa2.date)
    FROM
      Player_Attributes pa2
    WHERE
      pa2.player_api_id = pa.player_api_id
  );
