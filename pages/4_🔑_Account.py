import streamlit as st
from utils.db import execute_query

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


def create_account(username, password):
    print("Creating account")

    create_query = """
    INSERT INTO User (username, password)
    VALUES (:username, :password);
    """

    execute_query(create_query, {"username": username, "password": password})

    st.success("Account created successfully!")
    st.markdown("Please login using your username and password")
    st.balloons()

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
            username = st.text_input("Enter your unique username")
            password = st.text_input("Password", type="password", key="Signup password")
            favorite_team = st.text_input("Enter your favorite soccer team")
            bio = st.text_area("Tell us about yourself")
            favorite_player = st.text_input("Enter your favorite player")
            favorite_match = st.text_input("Enter your favorite match")
            profile_picture = st.file_uploader(
                "Upload your profile picture", type=["png", "jpg", "jpeg"]
            )

            st.button(
                "Create My Account!",
                on_click=lambda: create_account(username, password),
            )

    # signed in so this will run
    else:
        st.success(f"You are logged in as {st.session_state.username}!")
        if st.button("Sign Out"):
            st.session_state.username = None
            st.rerun()


app()
