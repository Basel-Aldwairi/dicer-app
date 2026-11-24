import streamlit as st
from games_db import load_db


db = load_db()


match_history = db.select_view_all_rounds_winners()
headers = ('Round ID', 'Game', 'Winner')
match_history.insert(0, headers)
st.table(match_history,border='horizontal', width='stretch', hide_index=True)