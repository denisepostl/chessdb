"""
Module: test_connection.py

Module that contains tests for Connection class.

This module tests the functionality of the Connection class from the exporting module.

Author: Denise Postl
History: 20231121 12:10 Defined and Implemented Test Class

"""

import pytest
from src.exporting import Connection, ChessDBExporter

class TestConnection:
    """
    A class containing test cases for the Connection class.

    These tests validate the initialization and establishment of connections.
    """

    def test_connection_initialization(self):
        """
        Test the initialization of the Connection class with provided parameters.

        Checks if the Connection object is initialized with the correct attributes:
        - database
        - host
        - user
        - password
        - port
        """

        conn = Connection('chess1', 'localhost', 'postgres', 'test_password', '1234')
        assert conn.database == 'chess1'
        assert conn.host == 'localhost'
        assert conn.user == 'postgres'
        assert conn.password == 'test_password'
        assert conn.port == '1234'

    def test_connection_establishment(self):
        """
        Test the establishment of a connection using Connection's connect method.

        Ensures that a connection can be established successfully and the 'connection'
        attribute is not None after connecting. Also, closes the connection after the test.
        """

        conn = Connection('chess1', 'localhost', 'postgres', 'test_password', '1234')
        conn.connect()
        assert conn.connection is not None
        conn.close()
