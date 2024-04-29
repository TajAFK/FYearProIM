import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
from create_db import create_db


class TestDatabaseErrorHandling(unittest.TestCase):
    @patch('builtins.print')
    @patch('create_db.sqlite3.connect')
    def test_database_access_error(self, mock_connect, mock_print):
        """Test if error handling properly logs database access issues."""
        # Setup the connection mock to raise an OperationalError
        mock_connect.side_effect = sqlite3.OperationalError("Unable to open database file")

        create_db()  # Running the function, expecting it to handle the error

        # Check that a specific error message pattern was printed
        mock_print.assert_any_call("An error occurred:", sqlite3.OperationalError("Unable to open database file"))

    @patch('builtins.print')
    @patch('create_db.sqlite3.connect')
    def test_sql_execution_error(self, mock_connect, mock_print):
        """Test if error handling properly logs SQL execution errors."""
        mocked_con = MagicMock()
        mock_connect.return_value = mocked_con
        mocked_cur = MagicMock()
        mocked_con.cursor.return_value = mocked_cur
        mocked_cur.execute.side_effect = sqlite3.DatabaseError("SQL Error")

        create_db()  # Running the function, expecting it to handle the error

        # Check that a specific error message pattern was printed
        mock_print.assert_any_call("An error occurred:", sqlite3.DatabaseError("SQL Error"))


if __name__ == '__main__':
    unittest.main()
