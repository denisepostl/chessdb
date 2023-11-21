"""
Module: main.py

This module contains a class ChessDBExporter that facilitates exporting
data from a database to CSV file.

Author: Denise Postl
History: 20231114 16:28 Defined Class
         20231114 16:30 Added Constructor and defined db path
         20231114 16:33 Defined and implemented export_to_csv method
         20231121 07:59 Added Connection class and fixed psycopg connection to db
         20231121 08:24 Changed DB Port from 5432 to 1234
         20231121 12:10 Added and Implemented ChessDBExporter Class
"""

import psycopg2
import csv
from psycopg2 import sql

class Connection:
    """
    A class to manage the connection to a PostgreSQL database.

    Attributes
    ----------
    database : str
        The name of the database.
    host : str
        The host address of the database.
    user : str
        The username for authentication.
    password : str
        The password for authentication.
    port : str
        The port number for the database connection.
    connection : psycopg2.extensions.connection
        The connection object.
    """

    def __init__(self, database, host, user, password, port):
        """
        Initializes a Connection object with database connection details.

        Parameters
        ----------
        database : str
            The name of the database.
        host : str
            The host address of the database.
        user : str
            The username for authentication.
        password : str
            The password for authentication.
        port : str
            The port number for the database connection.
        """
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        self.connection = psycopg2.connect(
            database=self.database,
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def close(self):
        """
        Closes the connection to the PostgreSQL database if it's open.
        """
        if self.connection:
            self.connection.close()

class ChessDBExporter:
    """
    A class to export chess game data from a PostgreSQL database to a CSV file.

    Attributes
    ----------
    connection : Connection
        An instance of the Connection class representing the database connection.
    """

    def __init__(self, connection):
        """
        Initializes a ChessDBExporter object with a database connection.

        Parameters
        ----------
        connection : Connection
            An instance of the Connection class representing the database connection.
        """
        self.connection = connection

    def chess_game_query(self):
        """
        Returns the SQL query to fetch chess game data from the database.

        Returns
        -------
        psycopg2.sql.Composable
            The SQL query.
        """
        return sql.SQL("""
            SELECT
                game.id,
                game.event,
                game.round,
                game.site,
                game.start_date,
                game.status,
                p1.display_name as black_player,
                p2.display_name as white_player,
                move.pgn,
                player.expected,
                player.score,
                player.text
            FROM
                chess_game game
            JOIN
                player p1 ON game.black_player_id = p1.id
            JOIN
                player p2 ON game.white_player_id = p2.id
            JOIN
                chess_move move ON game.id = move.game_id
            JOIN
                chess_move_to_position movetp ON move.id = movetp.chess_move_id
            JOIN
                chess_position player ON movetp.chess_club_position_id = player.id;
        """)

    def execute_query_to_csv(self, query, output_file):
        """
        Executes the given SQL query and exports the result to a CSV file.

        Parameters
        ----------
        query : psycopg2.sql.Composable
            SQL query to be executed.
        output_file : str
            Path to the output CSV file.

        Notes
        -----
        If there is no established database connection, it prints an error message.
        """
        if not self.connection.connection:
            print("No connection established.")
            return

        cursor = self.connection.connection.cursor()
        
        try:
            cursor.execute(query)
            data = cursor.fetchall()

            with open(output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([i[0] for i in cursor.description])
                writer.writerows(data)
            
            print(f"Data exported to '{output_file}'")
        except Exception as e:
            print("Error during data extraction:", e)
        finally:
            cursor.close()

if __name__ == "__main__":
    conn = Connection('chess1', 'localhost', 'postgres', 'Kennwort1', '1234')
    conn.connect()

    chess_queries = ChessDBExporter(conn)

    chess_game_query = chess_queries.chess_game_query()

    chess_queries.execute_query_to_csv(chess_game_query, 'src/exporting/exported_data.csv')

    conn.close()