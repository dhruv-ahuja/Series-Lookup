import sqlite3
from config import db_file


class Database:
    """
    Context manager to make interacting with the database easier.

    Connects to the database, generates and returns the cursor to be used
    when performing database-related operations.
    """

    def __init__(self):
        self.file = db_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor

        # we won't be able to use any of the context manager's methods in the
        # `with` block in other parts of our app if we do not return the class
        # instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type, exc_val and exc_tb refer to the exception type, exception
        # value and exception traceback respectively
        self.conn.close()
