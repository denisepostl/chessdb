"""
This module handles the exporting of data from a SQLite
database using the ChessDBExporter class.

Author: Denise Postl
History: 20231114 17:02 Exported ChessDB Class
"""


from .main import ChessDBExporter, Connection

__exports__ = [
    ChessDBExporter,
    Connection
]
