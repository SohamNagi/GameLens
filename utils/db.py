import pandas as pd
from sqlalchemy import text
import streamlit as st
from streamlit.connections import SQLConnection


@st.cache_resource
def get_conn():
    print("Creating connection")
    return st.connection("soccer", type=SQLConnection)


def execute_query(query: str, params=None):
    with get_conn().session as s:
        result = s.execute(text(query), params)
    return result


def get_leagues():
    league_query = """
    SELECT 
        l.id as id,
        l.name as name
    FROM
        League l;
    """

    league_result = execute_query(league_query)
    return pd.DataFrame(league_result).set_index("id").to_dict(orient="index")


def get_matches_for_league(league_id):
    match_query = """
    SELECT 
        m.id as id,
        t1.team_long_name as home_team_name,
        t2.team_long_name as away_team_name
    FROM
        match m
    INNER JOIN League l ON m.league_id = l.id
    INNER JOIN team t1 ON m.home_team_api_id = t1.team_api_id
    INNER JOIN team t2 ON m.away_team_api_id = t2.team_api_id
    WHERE l.id = :league_id;
    """

    match_result = execute_query(match_query, {"league_id": league_id})
    return pd.DataFrame(match_result).set_index("id").to_dict(orient="index")
