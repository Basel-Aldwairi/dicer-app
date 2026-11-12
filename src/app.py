import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
import json
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

data_file = current_dir.parent / 'data' / 'data.json'


st.set_page_config(page_title='Dicer-App', layout="centered")


empty_data = {
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 0,
    10 : 0,
    11 : 0,
    12 : 0,
}


def get_data():

    try:
        data = json.load(open(data_file))

        print(data)
        return data
    except Exception as e:
        print(e)
        st.error("Data not available")
        return []






if 'add_data' not in st.session_state:
    st.session_state['add_data'] = []


st.title("Dicer-App")


cs = st.columns(2)

with cs[0]:
    if st.button("Get data"):
        st.session_state['add_data'] = get_data()

with cs[1]:
    if st.button('save_data'):
        json.dump(st.session_state['add_data'], open(data_file, 'w'))





c1, c2, c3 = st.columns(3)

with c1:
    if st.button("2"):
        st.session_state['add_data'].append(2)


    if st.button("3"):
        st.session_state['add_data'].append(3)

    if st.button("4"):
        st.session_state['add_data'].append(4)


    if st.button("5"):
        st.session_state['add_data'].append(5)

with c2:
    if st.button("6"):
        st.session_state['add_data'].append(6)

    if st.button("7"):
        st.session_state['add_data'].append(7)

    if st.button("8"):
        st.session_state['add_data'].append(8)

    if st.button("<"):
        if len(st.session_state['add_data']) > 0:
            last_data = st.session_state['add_data'].pop()


with c3:

    if st.button("9"):
        st.session_state['add_data'].append(9)

    if st.button("10"):
        st.session_state['add_data'].append(10)

    if st.button("11"):
        st.session_state['add_data'].append(11)

    if st.button("12"):
        st.session_state['add_data'].append(12)



if len(st.session_state['add_data']) > 0:
    fig, ax = plt.subplots()

    ax.hist(st.session_state['add_data'])

    st.pyplot(fig)

