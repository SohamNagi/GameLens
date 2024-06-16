import streamlit as st
from utils.db import get_conn
import pandas as pd

st.set_page_config(page_title="Match", page_icon="🥅")

PLAYER_ID_PARAM = "player_id"

player_id = st.query_params.get(PLAYER_ID_PARAM)


def set_player_id():
    with get_conn().session as s:
        random_id_query = "SELECT id FROM player ORDER BY RANDOM() LIMIT 1;"
        random_id_result = s.execute(random_id_query)
        random_id = random_id_result.first()[0]

    st.query_params[PLAYER_ID_PARAM] = random_id


def main():
    # Explore players path
    if player_id is None:
        st.button("Random player", on_click=set_player_id)
        return

    with get_conn().session as s:
        player_query = """
        SELECT 
            p.id,
            p.player_name as name
        FROM
            player p
        WHERE p.id = :player_id;
        """

        player_result = s.execute(player_query, {"player_id": player_id})
        player = pd.DataFrame(player_result).iloc[0]

    st.header(f"Player {player['id']} details")

    st.metric(
        "Name",
        player["name"],
    )


main()
