# controller handles all the execution process for the application

import sys

import sqlite3
import tmdbv3api

import series_lookup.app as app
import series_lookup.queries as queries
import series_lookup.database as db
import series_lookup.config as config
import series_lookup.updates as upd


def controller(conn: sqlite3.Connection, tmdb: tmdbv3api.TMDb, tv: tmdbv3api.TV):
    """
    Handles the app execution flow.
    """

    app.prerun_checks(conn, tmdb)

    user_intent = app.get_user_intent()

    if user_intent == 0:
        # user wishes to quit
        cleanup(conn)

    elif user_intent == 1:
        # user wants to save a show

        # get users input and search for the show
        search_results = app.search_for_show(tv)

        # return to the start menu
        if not search_results:
            # this will act as a pause for the user
            print("Going back to the main screen...")
            input("Press ENTER to continue...")

            controller(conn, tmdb, tv)

        # map the results to a dictionary
        show_index, result_count = app.process_results(search_results)

        # get users choice from the dictionary
        users_choice = app.get_users_choice(result_count)

        if not users_choice:
            # this will act as a pause for the user
            print("Going back to the main screen...")
            input("Press ENTER to continue...")

            controller(conn, tmdb, tv)

        # this is the user selected show to be saved into the db
        show = app.get_show_info(users_choice, show_index, config.tv)

        # now, to send the show to be saved into the db
        saved = queries.save_show(conn, show)

        if saved:
            print(f"Successfully saved {show.name} to the database!")
        else:
            print(f"Unable to save {show.name} to the database.")

        print("Going back to the main screen...")
        input("Press ENTER to continue...")

    elif user_intent == 2:
        # user wants to view the saved shows

        # get a list of all shows in the db
        shows_list = queries.get_shows(conn)

        # now, draw the tables to represent the data beautifully
        app.draw_table(shows_list)

        print("Going back to the main screen...")
        input("Press ENTER to continue...")

    else:
        # input 3, check for show updates

        # send all the stores in the db to be checked for updates
        shows_list = queries.get_shows(conn)
        shows_with_updates = upd.check_updates(tv, shows_list)

        # push notifications for all shows with new seasons
        upd.send_update_notification(shows_with_updates)

        print("Going back to the main screen...")
        input("Press ENTER to continue...")


def cleanup(conn: sqlite3.Connection):
    """
    Performs the necessary cleanup before terminating the application.
    """

    conn.close()
    print("exiting...")
    input("Press ENTER to continue...")
    sys.exit()
