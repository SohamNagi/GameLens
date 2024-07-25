import streamlit as st
import pandas as pd
from utils.db import execute_query
import numpy as np
import cv2

PLAYERS_ID_PARAM = "players_id"

players_id = st.query_params.get(PLAYERS_ID_PARAM)


def check(username, password):
    check_query = """
        SELECT 
            u.username
        FROM User u
        WHERE u.username = :username AND u.password = :password;
        """

    result = execute_query(check_query, {"username": username, "password": password})
    user = result.fetchone()

    if user is None:
        st.error("Invalid username or password")
        return

    st.session_state.username = user.username
    st.rerun()


def create_account(
    username, password, favorite_team, favorite_player, bio, profile_picture
):
    print("Creating account")

    create_query = """
    INSERT INTO User (username, password)
    VALUES (:username, :password);
    """

    execute_query(create_query, {"username": username, "password": password})

    st.success("Account created successfully!")
    st.markdown("Please login using your username and password")
    st.balloons()

    if profile_picture is not None:
        file_bytes = np.asarray(bytearray(profile_picture.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        st.session_state.profile_picture = opencv_image

    st.session_state.bio = bio
    st.session_state.favorite_team = favorite_team
    st.session_state.favorite_player = favorite_player

    # if profile_picture is not None:
    #     img = Image.open(profile_picture)
    #     st.session_state.profile_picture = img
    #     st.image(
    #         img, caption="Uploaded Profile Picture", use_column_width=True
    #     )


def app():
    st.title("Welcome to GameLens!")

    # not signed in yet, so this will run first
    if "username" not in st.session_state:
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password", key="Login password")

            if st.button("Login!"):
                check(username, password)

        with signup_tab:
            get_teams_query = """
                SELECT DISTINCT Team.team_long_name as name
                FROM Team;
            """
            teams_result = execute_query(get_teams_query)
            teams_list = pd.DataFrame(teams_result)["name"].tolist()

            get_players_query = """
                SELECT DISTINCT Player.player_name as name
                FROM Player;
            """
            players_result = execute_query(get_players_query)
            players_list = pd.DataFrame(players_result)["name"].tolist()

            username = st.text_input("Enter your unique username")
            password = st.text_input("Password", type="password", key="Signup password")

            favorite_team = st.selectbox("Select your favorite team", teams_list)
            favorite_player = st.selectbox("Select your favorite player", players_list)

            bio = st.text_area("Tell us about yourself")
            profile_picture = st.file_uploader(
                "Upload your profile picture", type=["png", "jpg", "jpeg"]
            )

            st.button(
                "Create My Account!",
                on_click=lambda: create_account(
                    username,
                    password,
                    favorite_team,
                    favorite_player,
                    bio,
                    profile_picture,
                ),
            )

    # signed in so this will run
    else:
        st.success(f"You are logged in as {st.session_state.username}!")

        st.markdown("## Your profile")
        st.markdown(f"Your favorite team is {st.session_state.favorite_team}")
        st.markdown(f"Your favorite player is {st.session_state.favorite_player}")
        st.markdown(f"Your bio is {st.session_state.bio}")

        st.write("1 user(s) have the same favourite player as you")
        st.write("1 user(s) have the same favourite team as you")

        if st.session_state.get("profile_picture") is not None:
            st.markdown("## Your profile picture")
            st.image(
                st.session_state.profile_picture,
                width=500,
            )

        if st.button("Sign Out"):
            st.session_state.username = None
            st.rerun()


app()
