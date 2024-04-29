import unittest
from create_db import create_db
import sqlite3

class TestDatabaseIdempotency(unittest.TestCase):
    def test_idempotency_of_create_db(self):
        """
        Tests if multiple calls to create_db result in the same database schema using an in-memory database.
        """
        db_path = ':memory:'  # Use an in-memory database
        create_db(db_path)  # First initialization
        schema_after_first_init = self.get_db_schema(db_path)

        create_db(db_path)  # Second initialization
        schema_after_second_init = self.get_db_schema(db_path)

        self.assertEqual(schema_after_first_init, schema_after_second_init,
                         "Database schema should not change after multiple initializations.")

    def get_db_schema(self, db_path):
        """
        Fetches and returns the database schema as a sorted list of SQL table definitions.
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
            return sorted(row[0] for row in cursor.fetchall())

if __name__ == '__main__':
    unittest.main()
