from typing import List
from time import sleep

import tmdbv3api
from notifypy import Notify

import series_lookup.app as app

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

    for show in shows_with_updates:
        notif.message = (
            f"season {show.seasons} of {show.name} is now airing. Check it out!"
        )
        notif.send()
        sleep(1)
