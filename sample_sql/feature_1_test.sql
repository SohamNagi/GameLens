SELECT
    COUNT(fav_player) as fav_players_count
FROM
    users
WHERE
    fav_player = "Borja Mayoral"
