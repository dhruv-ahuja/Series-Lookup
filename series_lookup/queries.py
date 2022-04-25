# all functions that query data to and fro the database

from typing import List, Tuple

import sqlite3

from series_lookup.app import Show
import series_lookup.database as database
import series_lookup.exceptions as exceptions


def save_to_db(db_path: str, show: Show):
    """
    Save the show to the database.
    """

    query = "INSERT INTO show_data (name, seasons) VALUES (?, ?)"

    with database.ContextManager(db_path) as db:
        try:
            db.cursor.execute(query, [show.name, show.seasons])
            db.conn.commit()
        except sqlite3.Error as e:
            raise exceptions.DatabaseError(e)

        else:
            print(f"Successfully saved {show.name} to the database!\n")


def get_show(db_path: str, show_name: str) -> Tuple[int, sqlite3.Error]:
    """
    Check for the existence of a particular TV Show
    in the database.
    """

    query = "SELECT seasons FROM show_data WHERE name=?;"

    with database.ContextManager(db_path) as db:
        try:
            db.cursor.execute(query, [show_name])
        except sqlite3.Error as e:
            return (0, e)
        else:
            seasons = db.cursor.fetchone()
            return (seasons, None)


def get_shows(db_path: str) -> Tuple[List[Show], sqlite3.Error]:
    """
    Get a list of all the shows saved in the database.
    """

    shows: List[Show] = []

    query = "SELECT name, seasons FROM show_data;"

    with database.ContextManager(db_path) as db:
        try:
            db.cursor.execute(query)
        except sqlite3.Error as e:
            return ([], e)
        else:
            fetched_data = db.cursor.fetchall()

    for entry in fetched_data:
        shows.append(Show(entry[0], entry[1]))

    return (shows, None)
