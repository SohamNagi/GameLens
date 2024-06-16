import streamlit as st
from utils.db import get_conn
import pandas as pd

st.set_page_config(page_title="Match", page_icon="🥅")

MATCH_ID_PARAM = "match_id"

match_id = st.query_params.get(MATCH_ID_PARAM)


def set_match_id():
    with get_conn().session as s:
        random_id_query = "SELECT id FROM match ORDER BY RANDOM() LIMIT 1;"
        random_id_result = s.execute(random_id_query)
        random_id = random_id_result.first()[0]

    st.query_params[MATCH_ID_PARAM] = random_id


def main():
    # Explore matches path
    st.button("Random match", on_click=set_match_id)

    if match_id is None:
        return

    with get_conn().session as s:
        match_query = """
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
        WHERE m.id = :match_id;
        """

        match_result = s.execute(match_query, {"match_id": match_id})
        match = pd.DataFrame(match_result).iloc[0]

    print(match)

    st.header(f"Match {match['id']} details")

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
