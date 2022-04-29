from typing import List
from time import sleep

import tmdbv3api
from notifypy import Notify
import schedule
import sqlite3

import series_lookup.app as app
import series_lookup.queries as queries
import series_lookup.updates as upd
import series_lookup.database as db
import series_lookup.config as config

# we will check for show updates for all the shows list
def check_updates(tv: tmdbv3api.TV, shows_list: List[app.Show]) -> List[app.Show]:
    """
    Check for updates for all the shows stored in the database.
    """

    if not shows_list:
        print(
            "There is no saved data! \
Please save a show first before checking for update!"
        )

        return

    shows_with_updates: List[app.Show] = []

    print("Checking for updates...")

    for show in shows_list:
        check_seasons = tv.details(show.show_id)["number_of_seasons"]

        if check_seasons > show.seasons:
            show.seasons = check_seasons
            shows_with_updates.append(show)

    return shows_with_updates


def send_update_notification(shows_with_updates: List[app.Show]):
    """
    Send notifications to the user if there have been any updates to the shows.
    """

    notif = Notify()
    notif.application_name = "Series-Lookup"
    notif.title = "New Show Update!"

    if not shows_with_updates:
        print("All shows are up-to-date.")

    else:
        for show in shows_with_updates:
            notif.message = (
                f"season {show.seasons} of {show.name} is now airing. Check it out!"
            )
            notif.send()
            sleep(1)
