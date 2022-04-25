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


# make_table is to be run during the pre-run check
def make_table(db_path: str) -> sqlite3.Error:
    """
    Creates the "show_data" table to be used for storing the app's data if it doesn't yet exist.
    """

    query = """
    CREATE TABLE IF NOT EXISTS show_data(
        id integer PRIMARY KEY, 
        name text NOT NULL UNIQUE, 
        seasons integer NOT NULL UNIQUE
    );
    """

    with ContextManager(db_path) as db:
        try:
            db.cursor.execute(query)
        except sqlite3.Error as e:
            return e
        else:
            return None
