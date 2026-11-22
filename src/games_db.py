import sqlite3
import streamlit as st
import sql_queries
import pathlib



class Database:
    def __init__(self):

        file = pathlib.Path(__file__).parent.parent / 'data' / 'games.db'

        self.connection = sqlite3.connect(file, check_same_thread=False)
        self.execute(sql_queries.PRAGMA_FOREIGN_KEY)



    def initialize_db(self):
        self.create_dice_table()
        self.create_players_table()
        self.create_games_table()
        self.create_rounds_table()
        self.create_round_players_table()
        self.create_rounds_rolls_table()

        self.create_view_game_dice()


    def fill_db(self):

        dice = ['1D6',
                '2D6',
                'D20',
                'No Dice']

        for die in dice:
            self.insert_dice(die)

        games = [('Catan', 2),
                 ('Here to Slay', 2),
                 ('Flip 7', 3),
                 ('Scout', 3), ]

        for game in games:
            self.insert_games(*game)

        players = ['Basel', 'Yazan', 'Yazeed', 'Yousef']
        for player in players:
            self.insert_players(player)


    def close(self):
        self.connection.commit()
        self.connection.close()


    def execute(self, query, values =()):
        cursor = self.connection.cursor()
        results = cursor.execute(query, values).fetchall()
        cursor.close()
        return results


    def create_games_table(self):
        self.execute(sql_queries.GAMES_CREATE_TABLE)
        self.connection.commit()


    def drop_games_table(self):
        self.execute(sql_queries.GAMES_DROP_TABLE)
        self.connection.commit()


    def insert_games(self, game_name, dice_name):

        game_names = self.select_games()

        for game in game_names:
            if game[1] == game_name:
                return

        dice_id = self.select_dice_id(dice_name)

        self.execute(sql_queries.GAMES_INSERT_VALUES, (game_name, dice_id))
        self.connection.commit()


    def select_games(self):
        return self.execute(sql_queries.GAMES_SELECT)


    def print_games(self):
        results = self.select_games()
        for row in results:
            print(row)


    def delete_games(self, name):
        self.execute(sql_queries.GAMES_DELETE_VALUE, (name,))
        self.connection.commit()


    def select_game_id(self, name):
        result = self.execute(sql_queries.SELECT_GAME_ID, (name,))

        return result[0][0]


    def create_rounds_table(self):
        self.execute(sql_queries.ROUNDS_CREATE_TABLE)
        self.connection.commit()


    def insert_rounds(self, game_id, winner_id):
        cursor = self.connection.cursor()
        cursor.execute(sql_queries.ROUNDS_INSERT_VALUES, (game_id, winner_id))
        self.connection.commit()

        round_id = cursor.lastrowid
        cursor.close()
        return round_id


    def select_rounds(self):
        results = self.execute(sql_queries.SELECT_ROUNDS)
        return results


    def print_rounds(self):
        results = self.select_rounds()
        for row in results:
            print(row)


    def drop_rounds_table(self):
        self.execute(sql_queries.ROUNDS_DROP_TABLE)
        self.connection.commit()


    def delete_rounds(self, round_id):
        self.execute(sql_queries.ROUNDS_DELETE_VALUE, (round_id,))
        self.connection.commit()


    def create_dice_table(self):
        self.execute(sql_queries.DICE_CREATE_TABLE)
        self.connection.commit()

    def drop_dice_table(self):
        self.execute(sql_queries.DICE_DROP_TABLE)
        self.connection.commit()

    def insert_dice(self, dice_name):

        results = self.select_dice()

        for result in results:
            if result[1] == dice_name:
                return

        self.execute(sql_queries.DICE_INSERT_VALUES, (dice_name, ))
        self.connection.commit()

    def select_dice(self):
        results = self.execute(sql_queries.SELECT_DICE)
        return results

    def print_dice(self):
        results = self.select_dice()
        for row in results:
            print(row)

    def delete_dice_name(self, dice_name):
        dice_id = self.select_dice_id(dice_name)
        self.delete_dice(dice_id)


    def delete_dice(self, dice_id):
        self.execute(sql_queries.DICE_DELETE_VALUE, (dice_id,))
        self.connection.commit()

    def select_dice_id(self, dice_name):
        results = self.execute(sql_queries.SELECT_DICE_ID, (dice_name,))
        return results[0][0]

    def create_players_table(self):
        self.execute(sql_queries.PLAYERS_CREATE_TABLE)
        self.connection.commit()

    def drop_players_table(self):
        self.execute(sql_queries.PLAYERS_DROP_TABLE)
        self.connection.commit()

    def insert_players(self, player_name):

        results = self.select_players()

        for result in results:
            if result[1] == player_name:
                return

        self.execute(sql_queries.PLAYERS_INSERT_VALUES,(player_name,))
        self.connection.commit()

    def delete_players(self, player_id):
        self.execute(sql_queries.PLAYERS_DELETE_VALUE,(player_id,))
        self.connection.commit()

    def delete_players_name(self,player_name):
        player_id = self.select_player_id(player_name)
        self.delete_players(player_id)

    def select_players(self):
        results = self.execute(sql_queries.SELECT_PLAYERS)
        return results

    def print_players(self):
        results = self.select_players()
        for row in results:
            print(row)

    def select_player_id(self, player_name):
        results = self.execute(sql_queries.SELECT_PLAYERS_ID, (player_name,))
        return results[0][0]

    def create_rounds_rolls_table(self):
        self.execute(sql_queries.ROUNDS_ROLLS_CREATE_TABLE)
        self.connection.commit()

    def drop_rounds_rolls_table(self):
        self.execute(sql_queries.ROUNDS_ROLLS_DROP_TABLE)
        self.connection.commit()

    def insert_rounds_rolls(self, round_id, roll, count):
        self.execute(sql_queries.ROUNDS_ROLLS_INSERT_VALUES, (round_id, roll, count))
        self.connection.commit()

    def delete_rounds_rolls(self, round_id, roll):
        self.execute(sql_queries.ROUNDS_ROLLS_DELETE_VALUES, (round_id, roll))
        self.connection.commit()

    def select_rounds_rolls(self, round_id):
        results = self.execute(sql_queries.SELECT_ROUND_ROLLS, (round_id,))
        return results

    def select_all_rounds_rolls(self):
        results = self.execute(sql_queries.SELECT_ALL_ROUNDS_ROLLS)
        return results


    def print_rounds_rolls(self, round_id='all'):
        results = []

        if round_id == 'all':
            results = self.select_all_rounds_rolls()
        else:
            results = self.select_rounds_rolls(round_id)

        for row in results:
            print(row)


    def create_round_players_table(self):
        self.execute(sql_queries.ROUNDS_PLAYERS_CREATE_TABLE)
        self.connection.commit()

    def drop_round_players_table(self):
        self.execute(sql_queries.ROUNDS_PLAYERS_DROP_TABLE)
        self.connection.commit()

    def insert_round_players(self, round_id, player_name):
        self.execute(sql_queries.ROUNDS_PLAYERS_INSERT_VALUES, (round_id, player_name))
        self.connection.commit()

    def delete_round_players(self, round_id, player_name):
        self.execute(sql_queries.ROUNDS_PLAYERS_DELETE_VALUES, (round_id, player_name))
        self.connection.commit()

    def select_all_round_players(self):
        results = self.execute(sql_queries.SELECT_ALL_ROUNDS_PLAYERS)
        return results

    def print_round_players(self):
        results = self.select_all_round_players()
        for row in results:
            print(row)

    def create_view_game_dice(self):
        self.execute(sql_queries.CREATE_VIEW_GAME_DICE)
        self.connection.commit()

    def select_view_game_dice(self):
        results = self.execute(sql_queries.SELECT_GAME_DICE)
        return results

@st.cache_resource
def load_db() -> Database:
    return Database()
