# controller handles all the execution process for the application

import sys
from time import sleep

import sqlite3
import tmdbv3api
import schedule

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
            print("\nGoing back to the main screen...")
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
        show = app.get_show_info(users_choice, show_index, tv)

        # check whether the show exists in the db already or not
        _, show_id = queries.get_show(conn, show.name)

        if show_id != show.show_id:
            # now, to send the show to be saved into the db
            saved = queries.save_show(conn, show)

            if saved:
                print(f"Successfully saved {show.name} to the database!")
            else:
                print(f"Unable to save {show.name} to the database.")

        else:
            print(f"\n{show.name} already exists in the database!")

        print("\nGoing back to the main screen...")
        input("Press ENTER to continue...")

    elif user_intent == 2:
        # user wants to view the saved shows

        # get a list of all shows in the db
        shows_list = queries.get_shows(conn)

        # now, draw the tables to represent the data beautifully
        app.draw_table(shows_list)

        print("\nGoing back to the main screen...")
        input("Press ENTER to continue...")

    elif user_intent == 3:
        # input 3, check for show updates

        # send all the shows in the db to be checked for updates
        shows_list = queries.get_shows(conn)
        shows_with_updates = upd.check_updates(tv, shows_list)

        # send push notifications for all shows with new seasons
        upd.send_update_notification(shows_with_updates)

        print("\nGoing back to the main screen...")
        input("Press ENTER to continue...")

    else:
        # run as update-checker script
        print(
            "Started Update Checker. It will check for show updates/new seasons\
 every 30 mins."
        )

        update_checker_controller(conn, tmdb, tv)

        # implement the scheduler
        schedule.every(30).minutes.do(update_checker_controller)

        while True:
            schedule.run_pending()
            sleep(2)


# this function will help the module be run as a long-running script
# to check for show updates, like a cron job
def update_checker_controller(
    conn: sqlite3.Connection, tmdb: tmdbv3api.TMDb, tv: tmdbv3api.TV
):
    """
    Handles the script execution flow. The functions to check for updates
    here are run after a fixed interval of time, like a cron job would.
    """

    app.prerun_checks(conn, tmdb)

    # query for all the shows in the db
    shows_list = queries.get_shows(conn)

    # now, check which of these shows have new seasons/updates
    shows_with_updates = upd.check_updates(tv, shows_list)

    # send push notifications for all shows with new seasons
    upd.send_update_notification(shows_with_updates)


def cleanup(conn: sqlite3.Connection):
    """
    Performs the necessary cleanup before terminating the application.
    """

    conn.close()
    print("\nexiting...")
    input("Press ENTER to continue...")
    sys.exit()
