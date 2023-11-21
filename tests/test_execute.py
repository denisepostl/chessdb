"""
Module: test_execute.py

This module contains classes for exporting chess data to csv.

Author: Denise Postl
History: 20231121 12:40 Defined and Implemented Test Class

"""

import pytest
from src.exporting import ChessDBExporter, Connection

class TestChessDBExporter:
    """
    Test class for ChessDBExporter functionality.
    """

    @pytest.fixture
    def real_connection(self):
        """
        Fixture for establishing a real database connection.
        """
        connection = Connection('chess1', 'localhost', 'postgres', 'Kennwort1', '1234')
        connection.connect()
        yield connection
        connection.close()

    @pytest.fixture
    def chess_exporter(self, real_connection):
        """
        Fixture for creating a ChessDBExporter instance.
        """
        return ChessDBExporter(real_connection)

    def test_chess_game_query(self, chess_exporter):
        """
        Test chess_game_query method.
        
        Parameters
        ----------
        chess_exporter : ChessDBExporter
            Instance of ChessDBExporter.

        """
        query = chess_exporter.chess_game_query()
        assert query is not None

    def test_execute_query_to_csv_no_connection(self, capsys):
        """
        Test execute_query_to_csv method with no established connection.
        
        Parameters
        ----------
        capsys : pytest fixture
            Fixture for capturing stdout and stderr.

        """
        mock_connection = Connection('chess1', 'localhost', 'postgres', 'Kennwort1', '1234')
        exporter = ChessDBExporter(mock_connection)

        query = exporter.chess_game_query()
        output_file = 'test_output.csv'

        exporter.execute_query_to_csv(query, output_file)

        captured = capsys.readouterr()
        assert "No connection established." in captured.out

    def test_execute_query_to_csv_with_connection(self, real_connection, capsys):
        """
        Test execute_query_to_csv method with an established connection.
        
        Parameters
        ----------
        real_connection : pytest fixture
            Fixture for a real database connection.
        capsys : pytest fixture
            Fixture for capturing stdout and stderr.

        """
        exporter = ChessDBExporter(real_connection)

        query = exporter.chess_game_query()
        output_file = 'test_data/test_data.csv'

        exporter.execute_query_to_csv(query, output_file)

        captured = capsys.readouterr()
        assert f"Data exported to '{output_file}'" in captured.out