import streamlit as st
from utils.db import execute_query, get_conn
import pandas as pd
from PIL import Image

PLAYERS_ID_PARAM = "players_id"

players_id = st.query_params.get(PLAYERS_ID_PARAM)


def check(username, password):
    check_query = """
        SELECT 
            u.id
        FROM User u
        WHERE u.username = :username AND u.password = :password;
        """

    result = execute_query(check_query, {"username": username, "password": password})
    user = result.fetchone()

    if user is None:
        st.error("Invalid username or password")
        return

    st.session_state.user_id = user.id


def signoff():
    st.session_state.id = None


def app():
    st.title("Welcome to :yellow[GameLens!]")

    # not signed in yet, so this will run first
    if "id" not in st.session_state:
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password", key="Login password")
            st.button("Login!", on_click=lambda: check(username, password))

        with signup_tab:
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password", key="Signup password")
            username = st.text_input("Enter your unique username")
            favorite_team = st.text_input("Enter your favorite soccer team")
            bio = st.text_area("Tell us about yourself")
            favorite_player = st.text_input("Enter your favorite player")
            favorite_match = st.text_input("Enter your favorite match")
            profile_picture = st.file_uploader(
                "Upload your profile picture", type=["png", "jpg", "jpeg"]
            )

            if st.button("Create My Account!"):
                st.session_state.username = username
                st.session_state.useremail = email
                st.session_state.favorite_team = favorite_team
                st.session_state.bio = bio
                st.session_state.favorite_player = favorite_player
                st.session_state.favorite_match = favorite_match

                st.success("Account created successfully!")
                st.markdown("Please login using your email and password")
                st.balloons()

                if profile_picture is not None:
                    img = Image.open(profile_picture)
                    st.session_state.profile_picture = img
                    st.image(
                        img, caption="Uploaded Profile Picture", use_column_width=True
                    )

    # signed in so this will run
    if "id" in st.session_state:
        st.button("Sign Out", on_click=signoff)


app()
