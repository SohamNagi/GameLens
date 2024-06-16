import streamlit as st
from streamlit.connections import SQLConnection


@st.cache_resource
def get_conn():
    print("Creating connection")
    return st.connection("soccer", type=SQLConnection)
