from tmdbv3api import TMDb, TV
import os
from sys import exit
import csv
from dotenv import load_dotenv
from win10toast_persist import ToastNotifier


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
        id = int(data[2])

        check_seasons = tv.details(id)["number_of_seasons"]

        # now, only push the check_update integer into the list if
        # the show received an update, else scrape it
        if check_seasons > curr_seasons:
            new_seasons.append(name, curr_seasons, id)

        print(name, check_seasons)


if __name__ == "__main__":
    read_csv = read_data()

    if read_csv == []:
        quit()

    updates = get_updates(read_csv)
