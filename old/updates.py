import os
import csv
import pandas
import schedule
import app.config as config
from time import sleep
from win10toast_persist import ToastNotifier


tmdb = config.tmdb

db_file = config.db_file

tv = config.tv


class Updates:
    def read_data(self):
        """
        Read the database and collect show information for further use by other methods.
        """

        # using os' "getsize" method to check if the user has saved any tv shows
        check_for_db = os.path.getsize(db_file)

        if not check_for_db:
            # if the db file does not exist, print an error message and exit
            print("There is no saved data! Please save a show first before accessing!")

            return []

        with open(db_file, "r+", newline="") as file:
            reader = csv.reader(file)

            # ignore the header
            fields = next(reader)

            shows_data = [info for info in reader]

        return shows_data

    def get_updates(self, shows_data):
        """
        Use the tmdb api to search for updates for the shows stored in the local database.
        """

        if shows_data == []:
            print("There is no saved data! Please save a show first before accessing!")

            return

        new_seasons = []

        for data in shows_data:
            name = data[0]
            curr_seasons = int(data[1])
            tmdb_id = int(data[2])

            try:
                check_seasons = tv.details(tmdb_id)["number_of_seasons"]

            except:
                print("Please enter an API key first!")

                return

            # now, only push the check_update integer into the list if
            # the show received an update, else scrape it
            if check_seasons > curr_seasons:
                new_seasons.append((name, check_seasons, tmdb_id))

        return new_seasons

    def update_db(self, new_seasons):
        """
        Update the data for the TV show(s) in the database if there has been an update.
        """
        if new_seasons == []:
            return

        elif new_seasons is None:
            return

        # we'll use pandas to convert the csv to a dataframe, make needed changes and then convert it back
        csv_df = pandas.read_csv(db_file)

        for data in new_seasons:
            name, seasons = data[0], data[1]

            # using loc to specify what cell data to look for
            # if show name == name in the list, then set the new season count
            csv_df.loc[csv_df["Show Name"] == name, "Seasons"] = f"{str(seasons)}"

        # write changes to the file
        csv_df.to_csv(db_file, index=False)

    def send_notification(self, new_seasons):
        """
        Send toast notifications to the user if there have been updates.
        """

        notifier = ToastNotifier()

        if new_seasons is None:
            return

        if new_seasons == []:
            print("No updates.")
            return

        count = 0

        for data in new_seasons:

            # duration=None makes the notification persist
            notifier.show_toast(
                "New Season Alert!",
                f"The show {data[0]} has a new season!",
                duration=None,
            )

            sleep(7)

            count = count + 1

        # send an overview notification
        notifier.show_toast("Overview", f"{count} updates.", duration=None)


def main():
    updates = Updates()
    read_csv = updates.read_data()

    if read_csv != []:
        get_updates = updates.get_updates(read_csv)

        if get_updates is not None:
            save_updates = updates.update_db(get_updates)

            notifier = updates.send_notification(get_updates)


if __name__ == "__main__":

    print("Started Update Checker; will check for updates every half an hour.")

    # check for an update initially
    main()

    # implement the schedule library to emulate a cron job
    schedule.every(30).minutes.do(main)
    while True:
        schedule.run_pending()
        sleep(2)
