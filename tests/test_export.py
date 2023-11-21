import os
import pytest
import csv
from exporting import Connection, ChessDBExporter
import psycopg2.extras

@pytest.fixture
def in_memory_db():
    """
    Fixture creating an in-memory SQLite database for testing purposes.

    Returns
    -------
    psycopg2.extensions.connection
        A connection to the in-memory database.
    """
    connection = psycopg2.connect(database=':memory:', host='localhost', user='postgres', password='password', port='1234')
    yield connection
    connection.close()

@pytest.fixture
def chess_exporter(in_memory_db):
    """
    Fixture creating an instance of ChessDBExporter using an in-memory database connection for testing purposes.

    Returns
    -------
    ChessDBExporter
        An instance of ChessDBExporter for testing.
    """
    conn = Connection(database='chess1', host='localhost', user='postgres', password='password', port='1234')
    conn.connection = in_memory_db
    return ChessDBExporter(conn)

def test_chess_game_query(chess_exporter):
    """
    Test if the chess_game_query method generates a valid SQL query.

    Parameters
    ----------
    chess_exporter : ChessDBExporter
        An instance of ChessDBExporter.
    """
    query = chess_exporter.chess_game_query()
    assert isinstance(query, psycopg2.sql.Composable)

def test_execute_query_to_csv(chess_exporter):
    """
    Test if execute_query_to_csv method exports data to a CSV file.

    Parameters
    ----------
    chess_exporter : ChessDBExporter
        An instance of ChessDBExporter.
    """
    chess_exporter.connection.connection.set_client_encoding('UTF8')
    with chess_exporter.connection.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("""
            CREATE TABLE chess_game (
                id SERIAL PRIMARY KEY,
                event VARCHAR(100),
                round INTEGER,
                site VARCHAR(100),
                start_date DATE,
                status INTEGER,
                black_player_id INTEGER,
                white_player_id INTEGER
            );
            INSERT INTO chess_game (event, round, site, start_date, status, black_player_id, white_player_id)
            VALUES ('Test Event', 1, 'Test Site', '2023-11-21', 1, 1, 2);
        """)

    output_file = 'test_data/exported_test_data.csv'
    query = chess_exporter.chess_game_query()
    chess_exporter.execute_query_to_csv(query, output_file)

    assert os.path.exists(output_file)

    with open(output_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        assert len(data) == 2  
        assert data[0] == ['id', 'event', 'round', 'site', 'start_date', 'status', 'black_player', 'white_player', 'pgn', 'expected', 'score', 'text']
        assert data[1][1] == 'Test Event'
