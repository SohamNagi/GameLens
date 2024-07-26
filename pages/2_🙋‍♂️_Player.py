import streamlit as st
import pandas as pd
from utils.db import execute_query, get_players


st.set_page_config(page_title="Match", page_icon="🥅")

PLAYER_ID_PARAM = "player_id"

player_id = st.query_params.get(PLAYER_ID_PARAM)

df = pd.read_csv("male_players.csv")


def get_player_stat(fifa_api_id, column):
    try:
        value = df.loc[df['player_fifa_api_id']
                       == fifa_api_id, column].values[0]
        return value
    except IndexError:
        return "NULL"
    except KeyError:
        return "NULL"


def set_player_id(selected_player_id):
    st.query_params[PLAYER_ID_PARAM] = selected_player_id


def set_random_player_id():
    random_id_query = "SELECT id FROM player ORDER BY RANDOM() LIMIT 1;"
    random_id_result = execute_query(random_id_query)
    random_id = random_id_result.first()[0]
    st.query_params[PLAYER_ID_PARAM] = random_id


def main():
    # Explore players path
    st.button("Random player", on_click=set_random_player_id)

    if player_id is None:
        st.title("Pick a player")

        players = get_players()
        selected_player_id = st.selectbox(
            "Player",
            players.keys(),
            format_func=lambda x: players[x]["name"],
            on_change=lambda: set_player_id(selected_player_id),
        )

        return

    player_query = """
    SELECT
        p.id,
        p.height as height,
        p.weight as weight,
        p.player_name as name,
        p.player_fifa_api_id as fifaid,
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
    fid = player['fifaid']
    player_found = get_player_stat(fid, "short_name")
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
    if player_found != "NULL":
        # HTML and CSS for FIFA card
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=DIN+Condensed:wght@700&display=swap');
            .card {
                width: 395px;
                height: 600px;
                border-radius: 15px;
                text-align: center;
                background-image: url('https://i.ibb.co/C57HQyH/bg.png');
                background-size: cover;
                font-family: 'DIN Condensed', sans-serif;
                position: relative;
                color: black;
            }
            .rating, .position, .name {
                margin: 0;
            }
            .rating {
                font-size: 5em;
                position: absolute;
                top: 100px;
                left: 71px;
            }
            .position {
                font-size: 2em;
                position: absolute;
                top: 180px;
                left: 85px;
            }
            .player-img {
                width: 120px;
                height: 120px;
                position: absolute;
                top: 200px;
                left: 40%;
                scale:2
            }
            .name {
                font-size: 2.5em;
                position: absolute;
                bottom: 155px;
                left: 53%;
                transform: translateX(-50%);
            }
            .stats {
                position: absolute;
                bottom: 85px;
                left: 25px;
                width: 95%;
                padding: 5px 40px;
                display: flex;
                justify-content: space-between;
                font-size: 2.5em;
            }
            .stat {
                float: left;
                text-align: center;
            }
            .stats div {
                text-align: center;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

        # FIFA card content
        st.markdown(
            f"""
            <div class="card">
                <div class="rating">{get_player_stat(fid, 'overall')}</div>
                <div class="position">{get_player_stat(fid, 'player_positions')[0:2]}</div>
                <img src="{get_player_stat(fid, 'player_face_url')}" class="player-img">
                <div class="name">{get_player_stat(fid, 'short_name')}</div>
                <div class="stats">
                    <div class="stat">{str(get_player_stat(fid, 'pace'))[0:2]}</div>
                    <div class="stat">{str(get_player_stat(fid, 'shooting'))[0:2]}</div>
                    <div class="stat">{str(get_player_stat(fid, 'passing'))[0:2]}</div>
                    <div class="stat">{str(get_player_stat(fid, 'dribbling'))[0:2]}</div>
                    <div class="stat">{str(get_player_stat(fid, 'defending'))[0:2]}</div>
                    <div class="stat">{str(get_player_stat(fid, 'physic'))[0:2]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
main()
