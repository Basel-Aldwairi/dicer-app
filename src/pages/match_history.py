import pandas
import streamlit as st
from games_db import load_db
import pandas as pd

db = load_db()


match_history = db.select_view_all_rounds_winners()
if match_history:
    df = pandas.DataFrame(match_history)
    headers = ('Round ID', 'Time', 'Game', 'Winner')
    df.columns = headers
    st.table(df,border='horizontal', width='stretch', hide_index=True)\

else:
    st.warning('No match history found')