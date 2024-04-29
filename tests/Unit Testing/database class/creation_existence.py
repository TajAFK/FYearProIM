import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from create_db import create_db  # Adjust import as per your actual module and function name


class TestCreateDB(unittest.TestCase):
    @patch('sqlite3.connect')
    def test_table_creation_commands(self, mock_connect):
        """
        Tests if the `create_db` function issues the correct SQL table creation commands.
        This test uses mocking to intercept SQL executions and verifies that
        the expected commands were sent to the database.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        create_db()  # Call the function to test

        # List of expected SQL commands, simplified to check for key parts of the command.
        # This assumes the commands are the main part of each CREATE TABLE statement.
        expected_commands = [
            "CREATE TABLE IF NOT EXISTS employee",
            "CREATE TABLE IF NOT EXISTS supplier",
            "CREATE TABLE IF NOT EXISTS category",
            "CREATE TABLE IF NOT EXISTS product",
            "CREATE TABLE IF NOT EXISTS customers",
            "CREATE TABLE IF NOT EXISTS bills",
            "CREATE TABLE IF NOT EXISTS bill_items",
        ]

        executed_commands = [
            ' '.join(call[0][0].split())  # Normalize whitespace and line breaks
            for call in mock_cursor.execute.call_args_list
        ]

        for command in expected_commands:
            # Check each expected command is in one of the executed commands
            self.assertTrue(any(command in executed for executed in executed_commands),
                            f"Expected command not found: {command}")


if __name__ == '__main__':
    unittest.main()
