import sqlite3


class ContextManager:
    """
    Context manager to make interacting with the database easier.

    Connects to the database, generates and returns the cursor to be used
    when performing database-related operations.
    """

    def __init__(self, db_path):
        # file is our db file
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # we won't be able to use any of the context manager's methods in the
        # `with` block in other parts of our app if we do not return the class
        # instance
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type, exc_val and exc_tb refer to the exception type, exception
        # value and exception traceback respectively
        self.conn.close()


def make_table(db_path: str) -> bool:
    query = """
    CREATE TABLE IF NOT EXISTS show_data(
        id integer PRIMARY KEY, 
        name text NOT NULL, 
        seasons integer NOT NULL
    );
    """

    with ContextManager(db_path) as db:
        try:
            db.cursor.execute(query)
        except sqlite3.Error as e:
            print("error while trying to make table: ", e)
            return False
        else:
            return True
