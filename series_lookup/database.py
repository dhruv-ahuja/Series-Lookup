from typing import Tuple

import sqlite3


def connect_to_db(db_path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Forms a connection to a database given its path.
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        return (None, None)
    else:
        return (conn, cursor)


# make_table is to be run during the pre-run check
def make_table(cursor: sqlite3.Cursor) -> sqlite3.Error:
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
        cursor.execute(query)
    except sqlite3.Error as e:
        return e
    else:
        return None
