# all functions that query data to and from the database

from typing import List, Tuple

import sqlite3

from series_lookup.app import Show
import series_lookup.database as db


def save_show(conn: sqlite3.Connection, show: Show):
    """
    Save the show to the database.
    """

    query = "INSERT INTO show_data (name, seasons, show_id) VALUES (?, ?, ?)"

    saved = db.execute_query(conn, query, [show.name, show.seasons, show.show_id])

    return saved


def get_show(conn: sqlite3.Connection, show_name: str) -> Tuple[int, int]:
    """
    Check for the existence of a particular TV Show
    in the database.
    """

    query = "SELECT seasons, show_id FROM show_data WHERE name=?;"

    try:
        cursor = conn.cursor()
        cursor.execute(query, [show_name])
    except sqlite3.Error as e:
        print(f"Error fetching {show_name} data: ", e)
    else:
        show_data = cursor.fetchone()
    finally:
        cursor.close()

        return show_data if show_data else None


def get_shows(conn: sqlite3.Connection) -> List[Show]:
    """
    Get a list of all the shows saved in the database.
    """

    shows: List[Show] = []

    query = "SELECT name, seasons, show_id FROM show_data;"

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
        shows.append(Show(entry[0], entry[1], entry[2]))

    return shows


def rollback_transaction(cursor: sqlite3.Cursor, e: sqlite3.Error = None):
    """
    Helper function to handle the transaction rollback procedure.
    """

    if not e:
        print("Error updating show season count")
    else:
        print("Error updating show season count:", e)

    print("Rolling back transaction... ")

    cursor.execute("ROLLBACK;")
    cursor.close()


def update_shows(conn: sqlite3.Connection, shows_with_updates: List[Show]) -> bool:
    """
    Update all shows that have received a new season.
    """

    query = "UPDATE show_data SET seasons=? WHERE name=? RETURNING *;"

    cursor = conn.cursor()

    # begin transaction
    cursor.execute("BEGIN TRANSACTION;")

    success = True

    # execute the update query for all shows in the list
    for show in shows_with_updates:

        try:
            cursor.execute(query, [show.seasons, show.name])
        except sqlite3.Error as e:
            rollback_transaction(cursor, e)
            success = False
        else:
            # generally, update statements don't directly indicate an error
            # we have to compare the returning data from the query
            # and check for ourselves
            i = cursor.fetchone()
            if not i:
                rollback_transaction(cursor)
                success = False

        # if any previous query has failed, for whatever reason, no need to
        # continue the process
        if not success:
            break

    # if all queries are executed successfully, commit the transaction
    if success:
        cursor.execute("COMMIT;")
        cursor.close()

    return success
