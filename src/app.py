import streamlit as st
from matplotlib import pyplot as plt
import json
from pathlib import Path
from configs import *
from games_db import load_db

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

data_file = current_dir.parent / 'data' / 'data.json'


st.set_page_config(page_title='Dicer-App', layout="centered")


def get_data():

    try:
        data = json.load(open(data_file))

        print(data)
        return data
    except Exception as e:
        print(e)
        st.error("Data not available")
        return []



if 'data' not in st.session_state:
    st.session_state['data'] = []
if 'col_count' not in st.session_state:
    st.session_state['col_count'] = 3
if 'dice_rolls' not in st.session_state:
    st.session_state['dice_rolls'] = 12
if 'min_roll' not in st.session_state:
    st.session_state['min_roll'] = 2


db = load_db()

st.title("Dicer-App")


with st.sidebar:
    st.subheader('Dice Configs')


    st.session_state['col_count'] = st.slider('Column Count', min_value=1, max_value=4, value=3)

    used_dice = st.selectbox('Game Dice', options=list(dice_dict.keys()))

    if used_dice == 'Custom':
        rolls_values = st.slider('Possible Rolls', min_value=1, max_value=20,
                                 value=dice_dict['Custom'])
        st.session_state['min_roll'] = rolls_values[0]
        st.session_state['dice_rolls'] = rolls_values[1]
        dice_dict['Custom'] = (rolls_values[0], rolls_values[1])
    else:
        st.session_state['min_roll'] = dice_dict[used_dice][0]
        st.session_state['dice_rolls'] = dice_dict[used_dice][1]


    st.divider()


    cs = st.columns(2)

    with cs[0]:
        if st.button("Get data", use_container_width=True):
            st.session_state['data'] = get_data()

    with cs[1]:
        if st.button('save_data', use_container_width=True):
            json.dump(st.session_state['data'], open(data_file, 'w'))



st.divider()


col_count = st.session_state['col_count']
dice_rolls = st.session_state['dice_rolls']
min_roll = st.session_state['min_roll']

roll_cols = st.columns(col_count)

element_count = dice_rolls - min_roll + 2

roll = min_roll
delete_location = dice_rolls - min_roll if col_count == 3 and element_count % col_count == 0 else element_count - 1

for i in range(element_count):
    col = i % col_count

    with roll_cols[col]:
        if i == delete_location:
            if  st.button("<", use_container_width=True) and len(st.session_state['data']) > 0:
                last_data = st.session_state['data'].pop()

        else:
            if st.button(str(roll), use_container_width=True, key=str(i)):
                st.session_state['data'].append(roll)
            roll += 1



st.divider()


if len(st.session_state['data']) > 0:
    fig, ax = plt.subplots()

    ax.set_title(f"Total Rolls : {len(st.session_state['data'])}")
    ax.set_xlabel("Dice Numbers")
    ax.set_ylabel("Rolls")


    counts, bins, patches = ax.hist(
        st.session_state['data'],
        bins=range(st.session_state['min_roll'], st.session_state['dice_rolls']+2),
        align='left',
        edgecolor='black'
    )

    colors = [
        'red', 'orangered', 'darkorange', 'orange', 'gold',
        'yellowgreen', 'mediumseagreen', 'dodgerblue', 'mediumpurple',
        'orchid', 'hotpink'
    ]

    for i, patch in enumerate(patches):
        patch.set_facecolor(colors[i % len(colors)])

    ax.set_xticks(range(st.session_state['min_roll'], st.session_state['dice_rolls']+1))

    st.pyplot(fig)

