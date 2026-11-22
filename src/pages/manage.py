import dataclasses
from typing import Callable

import streamlit as st
from games_db import load_db
from dataclasses import dataclass


db = load_db()

@dataclass
class Tables:
    singular: str
    insert_method: Callable
    delete_method: Callable
    select_all_method: Callable

st.header('Managment')


st.sidebar.subheader('Table')




tables_list = {'Players' : Tables('Player', db.insert_players, db.delete_players_name, db.select_players),
                'Games' : Tables( 'Game', db.insert_games, db.delete_games, db.select_view_game_dice),
               'Dice' : Tables( 'Die', db.insert_dice, db.delete_dice_name, db.select_dice),
                }


if 'selected_table' not in st.session_state:
    st.session_state['selected_table'] = list(tables_list.keys())[0]

st.session_state['selected_table'] = st.sidebar.selectbox('Table to Magange', tables_list.keys())



col_count = 1
if st.session_state['selected_table'] == 'Games':
    col_count = 2

cols = st.columns(col_count)
with cols[0]:
    item_name = st.text_input(f'{tables_list[st.session_state['selected_table']].singular} Name')

if col_count > 1:
    with cols[1]:
        dice_name = st.text_input('Dice Name')

cols = st.columns(2)
with cols[0]:
    add_button =  st.button(f'Insert {tables_list[st.session_state['selected_table']].singular}', use_container_width=True)
    with cols[1]:
        remove_button = st.button(f'Remove {tables_list[st.session_state['selected_table']].singular}', use_container_width=True)

if st.session_state['selected_table'] == 'Games':
    items = (item_name, dice_name)
else:
    items = (item_name, )

if add_button and item_name != '':
    tables_list[st.session_state['selected_table']].insert_method(*items)

if remove_button and item_name != '':
    tables_list[st.session_state['selected_table']].delete_method(item_name)

st.divider()

st.table(tables_list[st.session_state['selected_table']].select_all_method(), border='horizontal', width='stretch', hide_index=True)