import streamlit as st
from utils.db import get_conn
import pandas as pd
from PIL import Image

PLAYERS_ID_PARAM = "players_id"

players_id = st.query_params.get(PLAYERS_ID_PARAM)

def check():
    try:
        st.write('Login Successfully')
        st.session_state.signedout = True
        st.session_state.signout = True
        
    except:
        st.warning('Login Failed')

def signoff():
    st.session_state.signout = False
    st.session_state.signedout = False
    st.session_state.username = ''
    st.session_state.useremail = ''
    st.session_state.favorite_team = ''
    st.session_state.bio = ''
    st.session_state.favorite_player = ''
    st.session_state.favorite_match = ''

def app():
    st.title('Welcome to :yellow[GameLens!]')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    if 'favorite_team' not in st.session_state:
        st.session_state.favorite_team = ''
    
    if 'bio' not in st.session_state:
        st.session_state.bio = ''

    if 'favorite_player' not in st.session_state:
        st.session_state.favorite_player = ''
    
    if 'favorite_match' not in st.session_state:
        st.session_state.favorite_match = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    # not signed in yet, so this will run first
    if not st.session_state.signedout:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')

            st.button('Login!', on_click=check)
    
        else:
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            username = st.text_input('Enter your unique username')
            favorite_team = st.text_input('Enter your favorite soccer team')
            bio = st.text_area('Tell us about yourself')
            favorite_player = st.text_input('Enter your favorite player')
            favorite_match = st.text_input('Enter your favorite match')
            profile_picture = st.file_uploader('Upload your profile picture', type=['png', 'jpg', 'jpeg'])

            if st.button('Create My Account!'):
                st.session_state.username = username
                st.session_state.useremail = email
                st.session_state.favorite_team = favorite_team
                st.session_state.bio = bio
                st.session_state.favorite_player = favorite_player
                st.session_state.favorite_match = favorite_match
                
                st.success('Account created successfully!')
                st.markdown('Please login using your email and password')
                st.balloons()

                if profile_picture is not None:
                    img = Image.open(profile_picture)
                    st.session_state.profile_picture = img
                    st.image(img, caption='Uploaded Profile Picture', use_column_width=True)

    # signed in so this will run
    if st.session_state.signout:
        st.text(f'Name: {st.session_state.username}')
        st.text(f'Email Id: {st.session_state.useremail}')
        st.text(f'Favorite Team: {st.session_state.favorite_team}')
        st.text(f'Bio: {st.session_state.bio}')
        st.text(f'Favorite Player: {st.session_state.favorite_player}')
        st.text(f'Favorite Match: {st.session_state.favorite_match}')
        if 'profile_picture' in st.session_state:
            st.image(st.session_state.profile_picture, caption='Profile Picture', use_column_width=True)
        st.button('Sign Out', on_click=signoff)

app()
