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

    with open("serie_db.csv", "r+", newline="") as file:
        reader = csv.reader(file)

        # ignore the header
        fields = next(reader)

        shows_data = [info for info in reader]

    return shows_data


def get_updates():
    


if __name__ == "__main__":
    read_data = read_data()
