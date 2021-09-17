import csv
from re import search
from tmdbv3api import TMDb, TV, Season, Search
from dotenv import load_dotenv
import os
from check_upd import *
from tabulate import tabulate
from sys import exit
import rich


class App:
    def __init__(self) -> None:
        # load environment variables
        load_dotenv()
        # initialize tmdb object
        self.tmdb = tmdb = TMDb()
        # feed api key
        tmdb.api_key = os.getenv("API_KEY")
        # config
        tmdb.language = "en"
        tmdb.debug = True

        self.tv = TV()

        # run CSV check method at app startup
        self.check_for_csv()

    def check_for_csv(self):
        """Creates a CSV file to store data if it does not yet exist"""

        # path to the CSV file
        path = ".\serie_db.csv"

        try:
            # check for the CSV file in the current working directory
            if not os.path.exists(path):
                print("Creating database file (first time user)")
                print("................................")

                # a simple context manager execution as "w" will create the file for us
                with open("serie_db.csv", "w") as file:
                    pass

                print("Database created")
                print()

        except OSError as e:
            print("Unable to create database file!")
            print()
            quit()

    def welcome(self):
        """The welcome screen of the app. Shows a list of options to the user, takes user input and feeds the input to other functions in the program."""

        print("Hello, what would you like to do?")

        print("Input 1 to enter a TV show into the local database.")
        print("Input 2 to view the shows stored in the local database")
        print("Input 3 to check for show updates.")

        ask_input = int(input("Else, input 0 to quit the program: "))

        return ask_input

    def search_for_show(self):
        """Look for the user-entered search term and return the results for further use by the 'results' method."""

        proper_search_term = False

        while not proper_search_term:
            search_results = self.tv.search(input("Enter the TV show to look for: "))

            if search_results != []:
                # the search was executed properly
                proper_search_term = True

            else:
                print(
                    "Your search term did not result in any results, please try again!"
                )

        print("Now scouring the TMDb database for results.")

        return search_results

    def print_results(self, search_results):
        """Prints the search results in a list manner, while hashing the appropriate data."""

        print("Showing the most relevant results.")
        print()

        list_len = len(search_results)

        show_index = {}

        for i in range(list_len):
            # map the shows in the list to a dictionary
            show_index[i + 1] = search_results

            # print the show name, year of origin and country of origin (CoO is in list form, print the 1st entry)
            print(
                f"{i + 1}. {search_results [i] ['name']},\
 {search_results [i] ['first_air_date'] [:4]},\
 {search_results [i] ['origin_country'] [0]}"
            )

        return show_index, list_len

    def get_user_choice(self, show_index, list_len):
        """Give the user a prompt to select their choice of TV show from the list generated by 'print_results' class method."""

        valid_choice = False

        print(
            "Input a number to select the show of your choice. Your choice will then be saved in the local database."
        )

        while not valid_choice:
            # giving users the option to go back since it can be a major hassle to be re-executing everything if you make a simple typo
            if list_len > 1:

                ask_choice = int(
                    input(
                        f"Enter a number between 1 and {list_len} or 0 if you want to go back: "
                    )
                )

            else:
                ask_choice = int(
                    input(
                        f"Enter 1 if you want to select the show or 0 if you want to go back: "
                    )
                )

            if 0 <= ask_choice <= list_len:
                valid_choice = True

        show_info = show_index[ask_choice]
        # the format is of a dict wrapped inside a list
        show_info = show_info[0]

        # we cannot get detailed information unless we use the show id
        show_name, show_id = show_info["name"], show_info["id"]

        # while searching a show by name gives a dict inside a list, searching a show by its id gives you a nested dictionary.
        season_count = self.tv.details(show_id)["number_of_seasons"]

        return show_name, season_count

    def write_to_csv(self, show_name, season_count):
        """This method saves the user-selected show to the CSV file."""


if __name__ == "__main__":
    # using a while loop here to keep executing the app until the user decides to quit
    app_persist = True

    while app_persist:
        app = App()
        init = app.welcome()

        if init == 1:

            search = app.search_for_show()

            print_results = app.print_results(search)

            user_choice = app.get_user_choice(*print_results)

            if user_choice == 0:
                print("Going back to the main screen.")
                break

            csv_writer = app.write_to_csv(user_choice)

        elif init == 0:
            exit()