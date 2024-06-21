-- Create temporary tables
CREATE TABLE TempCountry AS SELECT * FROM Country WHERE 1=0;
CREATE TABLE TempPlayer AS SELECT * FROM Player WHERE 1=0;
CREATE TABLE TempLeague AS SELECT * FROM League WHERE 1=0;
CREATE TABLE TempMatch AS SELECT * FROM Match WHERE 1=0;
CREATE TABLE TempPlayer_Attributes AS SELECT * FROM Player_Attributes WHERE 1=0;
CREATE TABLE TempUsers AS SELECT * FROM Users WHERE 1=0;

-- Insert data into temporary tables
-- League (No need to filter as we only want this league)
INSERT INTO TempLeague
SELECT * FROM League
WHERE id = 21518;

-- Matches associated with La Liga
INSERT INTO TempMatch
SELECT * FROM Match
WHERE league_id = 21518;

-- Players associated with La Liga matches
INSERT INTO TempPlayer
SELECT * FROM Player
WHERE player_api_id IN (
    SELECT home_player_1 FROM TempMatch
    UNION ALL
    SELECT home_player_2 FROM TempMatch
    UNION ALL
    SELECT home_player_3 FROM TempMatch
    UNION ALL
    SELECT home_player_4 FROM TempMatch
    UNION ALL
    SELECT home_player_5 FROM TempMatch
    UNION ALL
    SELECT home_player_6 FROM TempMatch
    UNION ALL
    SELECT home_player_7 FROM TempMatch
    UNION ALL
    SELECT home_player_8 FROM TempMatch
    UNION ALL
    SELECT home_player_9 FROM TempMatch
    UNION ALL
    SELECT home_player_10 FROM TempMatch
    UNION ALL
    SELECT home_player_11 FROM TempMatch
    UNION ALL
    SELECT away_player_1 FROM TempMatch
    UNION ALL
    SELECT away_player_2 FROM TempMatch
    UNION ALL
    SELECT away_player_3 FROM TempMatch
    UNION ALL
    SELECT away_player_4 FROM TempMatch
    UNION ALL
    SELECT away_player_5 FROM TempMatch
    UNION ALL
    SELECT away_player_6 FROM TempMatch
    UNION ALL
    SELECT away_player_7 FROM TempMatch
    UNION ALL
    SELECT away_player_8 FROM TempMatch
    UNION ALL
    SELECT away_player_9 FROM TempMatch
    UNION ALL
    SELECT away_player_10 FROM TempMatch
    UNION ALL
    SELECT away_player_11 FROM TempMatch
);

-- Player_Attributes
INSERT INTO TempPlayer_Attributes
SELECT * FROM Player_Attributes
WHERE player_api_id IN (
    SELECT player_api_id FROM TempPlayer
);

-- Users associated with La Liga players or teams
INSERT INTO TempUsers
SELECT * FROM Users
WHERE fav_team IN (SELECT home_team_api_id FROM TempMatch UNION SELECT away_team_api_id FROM TempMatch)
   OR fav_player IN (SELECT player_api_id FROM TempPlayer);

-- Country related to La Liga
INSERT INTO TempCountry
SELECT * FROM Country
WHERE id IN (SELECT DISTINCT country_id FROM TempMatch);

-- Drop old tables
DROP TABLE Country;
DROP TABLE Player;
DROP TABLE League;
DROP TABLE Match;
DROP TABLE Player_Attributes;
DROP TABLE Users;

-- Rename new tables to original names
ALTER TABLE TempCountry RENAME TO Country;
ALTER TABLE TempPlayer RENAME TO Player;
ALTER TABLE TempLeague RENAME TO League;
ALTER TABLE TempMatch RENAME TO Match;
ALTER TABLE TempPlayer_Attributes RENAME TO Player_Attributes;
ALTER TABLE TempUsers RENAME TO Users;
