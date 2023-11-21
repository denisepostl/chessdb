import pytest
from src.exporting import ChessDBExporter, Connection

@pytest.fixture
def connection():
    """
    Fixture to create a mocked database connection.
    
    Returns
    -------
    Connection:
        An instance of the Connection class for testing purposes.
    """
    mock_connection = Connection('chess1', 'localhost', 'postgres', 'test_password', '1234')
    mock_connection.connect()
    yield mock_connection
    mock_connection.close()

@pytest.fixture
def chess_exporter(connection):
    """
    Fixture to create a ChessDBExporter instance using a mocked database connection.
    
    Parameters
    ----------
    connection : Connection
        A mocked database connection.
    
    Returns
    -------
    ChessDBExporter:
        An instance of the ChessDBExporter class for testing purposes.
    """
    return ChessDBExporter(connection)

def test_chess_game_query(chess_exporter):
    """
    Test the chess_game_query method of ChessDBExporter.
    
    Parameters
    ----------
    chess_exporter : ChessDBExporter
        An instance of ChessDBExporter class.
    """
    query = chess_exporter.chess_game_query()
    assert query is not None
