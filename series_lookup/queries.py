# all functions that query data to and from the database

from typing import List

import sqlite3

from series_lookup.app import Show
import series_lookup.database as db


def save_to_db(conn: sqlite3.Connection, show: Show):
    """
    Save the show to the database.
    """

    query = "INSERT INTO show_data (name, seasons) VALUES (?, ?)"

    saved = db.execute_query(conn, query, [show.name, show.seasons])
    if saved:
        print(f"Successfully saved {show.name} to the database!\n")


def get_show(conn: sqlite3.Connection, show_name: str) -> int:
    """
    Check for the existence of a particular TV Show
    in the database.
    """

    query = "SELECT seasons FROM show_data WHERE name=?;"

    try:
        cursor = conn.cursor()
        cursor.execute(query, [show_name])
    except sqlite3.Error as e:
        print(f"Error fetching {show_name} data: ", e)
    else:
        seasons = cursor.fetchone()
    finally:
        cursor.close()
        # data from the db is queried within tuples, we only need the integer
        return seasons[0] if seasons else None


def get_shows(conn: sqlite3.Connection) -> List[Show]:
    """
    Get a list of all the shows saved in the database.
    """

    shows: List[Show] = []

    query = "SELECT name, seasons FROM show_data;"

    try:
        cursor = conn.cursor()
        cursor.execute(query)
    except sqlite3.Error as e:
        print("Error fetching all show data: ", e)
    else:
        fetched_data = cursor.fetchall()
    finally:
        cursor.close()

    for entry in fetched_data:
        shows.append(Show(entry[0], entry[1]))

    return shows
