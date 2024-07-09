import streamlit as st
from utils.db import execute_query, get_leagues, get_matches_for_league
import pandas as pd

st.set_page_config(page_title="Match", page_icon="🥅")

MATCH_ID_PARAM = "match_id"

match_id = st.query_params.get(MATCH_ID_PARAM)


def set_match_id(match_id):
    st.query_params[MATCH_ID_PARAM] = match_id


def set_random_match_id():
    random_id_query = "SELECT id FROM match ORDER BY RANDOM() LIMIT 1;"
    random_id_result = execute_query(random_id_query)
    random_id = random_id_result.first()[0]
    set_match_id(random_id)


def main():
    # Explore matches path

    if match_id is None:
        st.title("Pick a match")

        leagues = get_leagues()
        league_id = st.selectbox(
            "League",
            leagues.keys(),
            format_func=lambda x: leagues[x]["name"],
        )

        matches = get_matches_for_league(league_id)
        st.selectbox(
            "Match",
            matches.keys(),
            format_func=lambda x: f"{matches[x]['home_team_name']} vs {matches[x]['away_team_name']}",
            on_change=set_match_id,
        )

        st.subheader("Or pick a random match")
        st.button("Random match", on_click=set_random_match_id)

        return

    match_query = """
    SELECT 
        m.id,
        m.season,

        l.name as league_name,

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
    INNER JOIN League l ON m.league_id = l.id
    WHERE m.id = :match_id;
    """

    match_result = execute_query(match_query, {"match_id": match_id})
    match = pd.DataFrame(match_result).iloc[0]

    st.header(f"Match {match['id']} details")

    st.metric("League", match["league_name"])

    st.metric(
        "Home team",
        f"{match["home_team_name"]} - {match['home_team_goals']} goals",
    )

    st.metric(
        "Away team",
        f"{match['away_team_name']} - {match['away_team_goals']} goals",
    )

    st.metric("Season", match["season"])


main()
