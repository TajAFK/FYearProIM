import unittest
from unittest.mock import patch
import sqlite3

# Assuming your module is named `create_db` and the function `create_db` as well.
from create_db import create_db

class TestDatabaseErrorHandling(unittest.TestCase):
    @patch('builtins.print')  # Mocking the print function
    def test_database_access_error(self, mock_print):
        """Test if error handling properly logs database access issues."""
        with patch('create_db.sqlite3.connect', side_effect=sqlite3.OperationalError("Unable to open database file")):
            create_db()  # Running the function, expecting it to handle the error
            # Checking if print was called with the expected error message
            mock_print.assert_called_with("An error occurred:", sqlite3.OperationalError("Unable to open database file"))

    @patch('builtins.print')  # Mocking the print function
    def test_sql_execution_error(self, mock_print):
        """Test if error handling properly logs SQL execution errors."""
        with patch('create_db.sqlite3.connect') as mocked_connect:
            mocked_con = mocked_connect.return_value.__enter__.return_value
            mocked_cur = mocked_con.cursor.return_value
            mocked_cur.execute.side_effect = sqlite3.DatabaseError("SQL Error")
            create_db()  # Running the function, expecting it to handle the error
            # Checking if print was called with the expected error message
            mock_print.assert_called_with("An error occurred:", sqlite3.DatabaseError("SQL Error"))

if __name__ == '__main__':
    unittest.main()
