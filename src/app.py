import streamlit as st
from games_db import load_db
import streamlit.components.v1 as components


st.set_page_config(page_title='Dicer-App', layout="centered")

db = load_db()


if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'selected_game' not in st.session_state:
    st.session_state['selected_game'] = 'Catan'
if 'selected_players' not in st.session_state:
    st.session_state['selected_players'] = None
if 'round_id' not in st.session_state:
    st.session_state['round_id'] = None
if 'game_finished' not in st.session_state:
    st.session_state['game_finished'] = False
if 'last_game' not in st.session_state:
    st.session_state['last_game'] = None
if 'last_winners' not in st.session_state:
    st.session_state['last_winners'] = None

st.title("Dicer-App")

with st.sidebar:

    pass


st.divider()



players_list = [player[0] for player in db.select_players()]
games_list = [game[1] for game in db.select_games()]

selected_game = st.selectbox("Select Game", games_list, index=games_list.index(st.session_state['selected_game']))
selected_players = st.multiselect("Select Players", players_list, default=st.session_state['selected_players'] )

new_game_btn = st.button("New Game")


if new_game_btn:
    game_id = db.select_game_id(selected_game)
    round_id = db.insert_rounds(game_id)

    st.session_state['round_id'] = round_id
    st.session_state['selected_game'] = selected_game
    st.session_state['selected_players'] = selected_players

    db.insert_round_players_list(round_id, selected_players)

    st.success(f'Added a new Round to game "{selected_game}" with {', '.join(selected_players)}')

    st.session_state['game_started'] = True
    st.session_state['game_finished'] = False
    # st.session_state['selected_players'] = None
    st.session_state['last_game'] = None

if st.session_state['game_started']:
    st.session_state['last_winners'] = st.multiselect("Select Winner", st.session_state['selected_players'])

    update_winner_button = st.button("Update Winner")
    if update_winner_button:
        db.update_rounds_info(st.session_state['round_id'], list(st.session_state['last_winners']))
        st.session_state['last_game'] = st.session_state['selected_game']

        st.session_state['game_started'] = False
        st.session_state['round_id'] = None
        st.session_state['selected_players'] = None

        st.session_state['game_finished'] = True


if st.session_state['game_finished']:
    st.success(f'Updated Winner of game "{st.session_state['last_game']}" with {', '.join(st.session_state["last_winners"])}')


components.html(
    """
    <script>
    const doc = window.parent.document;

    function disableMobileKeyboard() {
        // Target inputs inside Streamlit's BaseWeb select/multiselect containers
        const inputs = doc.querySelectorAll('div[data-baseweb="select"] input');
        inputs.forEach(input => {
            if (input.inputMode !== 'none') {
                input.inputMode = 'none';
            }
        });
    }

    // Run immediately and observe DOM changes (for dynamic/conditional widgets)
    disableMobileKeyboard();
    const observer = new MutationObserver(disableMobileKeyboard);
    observer.observe(doc.body, { childList: true, subtree: true });
    </script>
    """,
    height=0,
    width=0,
)