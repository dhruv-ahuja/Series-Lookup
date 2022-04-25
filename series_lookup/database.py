from typing import Tuple

import sqlite3


def connect_to_db(db_path: str) -> sqlite3.Connection:
    """
    Forms a connection to a database given its path.
    """

    try:
        conn = sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)
    finally:
        return conn


# function to be used at the end of the application's execution
def cleanup_db_connection(conn: sqlite3.Connection):
    conn.close()


# make_table is to be run during the pre-run check
def make_table(conn: sqlite3.Connection):
    """
    Creates the "show_data" table to be used for storing the app's data
    if it doesn't yet exist.
    """

    query = """
    CREATE TABLE IF NOT EXISTS show_data(
        id integer PRIMARY KEY, 
        name text NOT NULL UNIQUE, 
        seasons integer NOT NULL UNIQUE
    );
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
