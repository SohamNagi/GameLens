import streamlit as st
import pandas as pd
from utils.db import get_conn
import random
country_list = [
    'Belgium', 'England', 'France', 'Germany', 'Italy', 
    'Netherlands', 'Poland', 'Portugal', 'Scotland', 'Spain', 
    'Switzerland'
]

# Function to get leagues from the database
def get_leagues():
    with get_conn().session as s:
        query = """
        SELECT 
            country.name AS country_name,
            league.name AS league_name
        FROM League
        LEFT JOIN Country
        ON country.id = league.country_id
        ORDER BY country.name
        """
        leagues_result = s.execute(query)
        leagues = leagues_result.fetchall()
    return leagues

def get_matches(country):
    with get_conn().session as s:
        query = f"""
            SELECT Match.id, 
                    Country.name AS country_name, 
                    League.name AS league_name, 
                    season, 
                    stage, 
                    date,
                    HT.team_long_name AS home_team,
                    AT.team_long_name AS away_team,
                    home_team_goal, 
                    away_team_goal                                        
            FROM Match
            JOIN Country on Country.id = Match.country_id
            JOIN League on League.id = Match.league_id
            LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
            LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
            WHERE country_name = '{country}'
            ORDER by date
            LIMIT 10
        """
        matches_result = s.execute(query)
        matches = matches_result.fetchall()
    return matches

st.set_page_config(page_title="Explore", page_icon="⚽")

st.button("Players") 
st.button("Teams Page")
if st.button("Match"):
    con = random.choice(country_list)
    matches = get_matches(con)
    matches_df = pd.DataFrame(matches, columns=[
        'Match ID', 'Country', 'League', 'Season', 'Stage', 'Date', 
        'Home Team', 'Away Team', 'Home Team Goals', 'Away Team Goals'
    ])
    st.write(f"### Matches in {con} in 2008/2009 Season")
    st.table(matches_df)
if st.button("Leagues"):
    leagues = get_leagues()
    # Convert the leagues data to a DataFrame
    leagues_df = pd.DataFrame(leagues, columns=['Country', 'League'])
    st.write("### Leagues")
    st.table(leagues_df)

