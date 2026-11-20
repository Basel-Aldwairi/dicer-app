import sqlite3
import sql_queries

class Database:
    def __init__(self):

        file = '../data/games.db'
        self.connection = sqlite3.connect(file)
        self.execute(sql_queries.PRAGMA_FOREIGN_KEY)


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


    def insert_games(self, game_name, dice_id):

        game_names = self.select_games()

        for game in game_names:
            if game[1] == game_name:
                return

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

        return result[0]


    def create_rounds_table(self):
        self.execute(sql_queries.ROUNDS_CREATE_TABLE)
        self.connection.commit()


    def insert_rounds(self, game_id, winner_id):
        self.execute(sql_queries.ROUNDS_INSERT_VALUES, (game_id, winner_id))
        self.connection.commit()


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

