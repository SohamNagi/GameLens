import streamlit as st
from utils.db import execute_query
import pandas as pd

st.set_page_config(page_title="Match", page_icon="🥅")

PLAYER_ID_PARAM = "player_id"

player_id = st.query_params.get(PLAYER_ID_PARAM)


def set_player_id():
    random_id_query = "SELECT id FROM player ORDER BY RANDOM() LIMIT 1;"
    random_id_result = execute_query(random_id_query)
    random_id = random_id_result.first()[0]

    st.query_params[PLAYER_ID_PARAM] = random_id


def main():
    # Explore players path
    st.button("Random player", on_click=set_player_id)

    if player_id is None:
        return

    player_query = """
    SELECT 
        p.id,
        p.height as height,
        p.weight as weight,
        p.player_name as name,
        pa.potential as potential,
        pa.overall_rating as rating,
        pa.preferred_foot as preferred_foot
    FROM
        player p
    INNER JOIN Player_Attributes pa ON p.player_api_id = pa.player_api_id
    WHERE p.id = :player_id;
    """

    player_result = execute_query(player_query, {"player_id": player_id})
    player = pd.DataFrame(player_result).iloc[0]

    st.header(f"Player {player['id']} details")

    basic, attributes = st.tabs(["Basic info", "Attributes"])

    with basic:
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Name",
                player["name"],
            )

        with col2:
            st.metric(
                "Height",
                f"{player['height']} cm",
            )

            st.metric(
                "Weight",
                f"{player['weight']} kg",
            )

    with attributes:
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Overall rating",
                player["rating"],
            )

        with col2:
            st.metric(
                "Potential",
                player["potential"],
            )

            st.metric(
                "Preferred foot",
                player["preferred_foot"],
            )


main()
