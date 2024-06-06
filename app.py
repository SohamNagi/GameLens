import streamlit as st

conn = st.connection("soccer", type="sql")

with conn.session as s:
    tables_query_result = s.execute("SELECT * FROM Match LIMIT 10;")
    tables_dataframe = st.dataframe(tables_query_result)


st.write("Hello world")
