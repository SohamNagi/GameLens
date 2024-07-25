import streamlit as st
import pandas as pd
from utils.db import execute_query

country_list = [
    'Belgium', 'England', 'France', 'Germany', 'Italy', 
    'Netherlands', 'Poland', 'Portugal', 'Scotland', 'Spain', 
    'Switzerland'
]

# Function to get leagues from the database
def get_leagues():
    query = """
        SELECT 
            country.name AS country_name,
            league.name AS league_name
        FROM League
        LEFT JOIN Country
        ON country.id = league.country_id
        ORDER BY country.name
        """
    leagues_result = execute_query(query)
    leagues = leagues_result.fetchall()
    return leagues

def get_matches(country):
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
            WHERE country_name = '{country}' AND Season = "2015/2016"
            ORDER by date ASC
            LIMIT 10
        """
    matches_result = execute_query(query)
    matches = matches_result.fetchall()
    return matches

def get_teams(country):
    query = f"""
            SELECT DISTINCT Team.team_long_name
            FROM Team
            JOIN Match ON Team.team_api_id = Match.away_team_api_id
            JOIN Country ON Match.country_id = Country.id
            WHERE Country.name = '{country}'
            ORDER BY Country.name, Team.team_long_name
        
        """
    teams_result = execute_query(query)
    teams = teams_result.fetchall()
    return teams

def get_players():
    query = """
                SELECT player_name
                FROM Player
                ORDER BY player_name
            """
    players_result = execute_query(query)
    players = players_result.fetchall()
    return players


#st.set_page_config(page_title="Explore", page_icon="⚽")

st.sidebar.title("Explore")
players_button = st.sidebar.button("Players")
teams_button = st.sidebar.button("Teams Page")
match_button = st.sidebar.button("Match")
leagues_button = st.sidebar.button("Leagues")
selected_country = st.selectbox('Select a country(Only for Match and Teams)', country_list)

if players_button:
    #search_query = st.text_input('Search for a player')
    players = get_players()
    players_df = pd.DataFrame(players,columns = ["Player name"])
    st.write("### ALL Players")
    st.table(players_df)


if teams_button and selected_country:
        teams = get_teams(selected_country)
        teams_df = pd.DataFrame(teams, columns = ["Team"])
        st.write(f"### Teams in {selected_country}")
        st.table(teams_df)

if match_button and selected_country:
        matches = get_matches(selected_country)
        matches_df = pd.DataFrame(matches, columns=[
            'Match ID', 'Country', 'League', 'Season', 'Stage', 'Date', 
            'Home Team', 'Away Team', 'Home Team Goals', 'Away Team Goals'
        ])
        st.write(f"### Matches in {selected_country}")
        st.table(matches_df)

if leagues_button:
    leagues = get_leagues()
    # Convert the leagues data to a DataFrame
    leagues_df = pd.DataFrame(leagues, columns=['Country', 'League'])
    st.write("###  ALL Leagues")
    st.table(leagues_df)

