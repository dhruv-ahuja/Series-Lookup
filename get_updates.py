from time import sleep
from tmdbv3api import TMDb, TV
import os
from sys import exit
import csv
from dotenv import load_dotenv
from win10toast_persist import ToastNotifier
import pandas


def read_data():
    """
    Read the database and collect show information for further use by other methods.
    """

    file_name = "serie_db.csv"

    # using os' "exists" method to check if the user has saved any tv shows
    check_for_db = os.path.exists(file_name)

    if not check_for_db:
        # if the db file does not exist, print an error message and exit
        print("There is no saved data! Please save a show first before accessing!")

        return []

    with open(file_name, "r+", newline="") as file:
        reader = csv.reader(file)

        # ignore the header
        fields = next(reader)

        shows_data = [info for info in reader]

    return shows_data


def get_updates(shows_data):
    """
    use the tmdb api to search for updates for the shows stored in the local database.
    """

    # load the .env file that stores our tmdb api key
    load_dotenv(dotenv_path="key.env")

    # instantiate the tmdb object
    tmdb = TMDb()
    tmdb.api_key = os.getenv("API_KEY")
    tmdb.debug = True

    tv = TV()

    new_seasons = []

    for data in shows_data:
        name = data[0]
        curr_seasons = int(data[1])
        tmdb_id = int(data[2])

        check_seasons = tv.details(tmdb_id)["number_of_seasons"]

        # now, only push the check_update integer into the list if
        # the show received an update, else scrape it
        if check_seasons > curr_seasons:
            new_seasons.append((name, check_seasons, tmdb_id))

    return new_seasons


def update_db(new_seasons):
    """
    Update the data for the TV show(s) in the database if there has been an update.
    """
    if new_seasons == []:
        return

    # we'll use pandas to convert the csv to a dataframe, make needed changes and then convert it back
    csv_df = pandas.read_csv("serie_db.csv")

    for data in new_seasons:
        name, seasons = data[0], data[1]

        # using loc to specify what cell data to look for
        # if show name == name in the list, then set the new season count
        csv_df.loc[csv_df["Show Name"] == name, "Seasons"] = f"{str(seasons)}"

    # write changes to the file
    csv_df.to_csv("serie_db.csv", index=False)


def send_notification(new_seasons):
    """
    Send toast notifications to the user if there have been updates.
    """

    if new_seasons == []:
        return

    notifier = ToastNotifier()

    count = 0

    for data in new_seasons:

        # duration=None makes the notification persist
        notifier.show_toast(
            "New Season Alert!", f"The show {data[0]} has a new season!", duration=None
        )

        sleep(8)

        count = count + 1

    # send an overview notification
    notifier.show_toast("Overview", f"{count} updates.", duration=None)


if __name__ == "__main__":
    read_csv = read_data()

    if read_csv == []:
        quit()

    updates = get_updates(read_csv)

    save_updates = update_db(updates)

    notifier = send_notification(updates)
