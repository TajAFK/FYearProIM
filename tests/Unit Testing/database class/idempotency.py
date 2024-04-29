import errno
import sqlite3
import unittest
from create_db import create_db
import os
import time


class TestDatabaseIdempotency(unittest.TestCase):
    def setUp(self):
        """
        Creates a temporary database file for testing.

        Note: It's important to use a temporary in-memory database when testing schema changes
              to avoid affecting your development or production database.
        """
        self.database_path = '../database class/sqltest.db'
        self.connection = sqlite3.connect(self.database_path)

    def tearDown(self):
        """
        Closes the database connection, and deletes the temporary test database file.
        """

        if self.connection:  # Check if connection exists
            try:
                self.connection.close()
            except Exception as e:  # Exception handling for robust closing
                print(f"Error closing database connection: {e}")

        try:
            os.remove(self.database_path)
        except OSError as e:
            if e.errno == errno.EACCES:  # Specific check for permission error
                time.sleep(0.2)  # Small delay
                os.remove(self.database_path)  # Retry deletion
            else:
                print(f"Error deleting database file: {e}")

    def test_idempotency_of_create_db(self):
        """
        Tests if multiple calls to create_db result in the same database schema.

        Idempotence means that an operation can be executed multiple times without
        changing the outcome beyond the initial application. This is important for
        database initialization functions to ensure stability.
        """
        create_db(self.database_path)  # First initialization
        schema_after_first_init = self.get_db_schema()

        create_db(self.database_path)  # Second initialization
        schema_after_second_init = self.get_db_schema()

        self.assertEqual(schema_after_first_init, schema_after_second_init,
                         "Database schema should not change after multiple initializations.")

    def get_db_schema(self):
        """
        Fetches and returns the database schema as a sorted list of SQL table definitions.

        Sorting ensures a consistent order for comparison in the test.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        return sorted(cursor.fetchall())

if __name__ == '__main__':
    unittest.main()
