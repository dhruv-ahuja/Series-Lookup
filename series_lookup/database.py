from typing import List, Tuple

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


def execute_query(conn: sqlite3.Connection, query: str, args: List = []) -> bool:
    """
    Helper function to run queries that don't require fetching data,
    against the database.
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query) if not args else cursor.execute(query, args)
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing query: ", e)
        return False
    else:
        return True
    # this is executed regardless of whether we return something or not!
    finally:
        cursor.close()


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
        seasons integer NOT NULL,
        show_id integer NOT NULL UNIQUE
    );
    """

    execute_query(conn, query)
