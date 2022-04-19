from typing import Tuple

import sqlite3

import series_lookup.exceptions as exceptions
import series_lookup.database as database
from series_lookup.config import db_path


def check_api_key(tmdb) -> bool:
    """
    Checks for the presence of the TMDB API Key.
    """

    return False if not tmdb.api_key or "" else True


def prerun_checks():
    """
    Executes all necessary methods before the main application
    logic is run.
    """

    api_key_exists = check_api_key()
    if not api_key_exists:
        raise exceptions.NoAPIKeyError(
            "You have not set a TMDB API Key! Please do so before \
using the application."
        )

    # run the table maker function
    err = database.make_table(db_path)
    if err:
        # supplying the error message received during the query operation to our custom exception
        raise exceptions.DatabaseError(err)


def get_user_intent() -> int:
    """
    The main interface of the app. Shows a list of options to the user and takes their input.
    """
    input_choices = {0, 1, 2, 3}

    print("Hello, what would you like to do?")
    print("Input 1 to enter a TV show into the local database.")
    print("Input 2 to view the shows stored in the local database")
    print("Input 3 to check for show updates.")
    print("Else, enter 0 to quit the program.")

    valid_input = False

    while not valid_input:
        ask_input = int(input("Enter your choice: "))

        if ask_input in input_choices:
            valid_input = True
        else:
            print("Invalid choice! Please try again.")

    return ask_input


def search_for_show(tv) -> list:
    """
    Look for the user-entered search term and return the results.
    """

    valid_input = False

    while not valid_input:
        search_term = input(
            "\nEnter the TV show to look for, or enter 0 \
to go back: "
        )
        if search_term == "0":
            return []

        search_results = tv.search(search_term)

        if not search_results:
            print("Your search did not result in any results, please try again!")

        else:
            valid_input = True

    if len(search_results) > 9:
        search_results = search_results[:8]

    return search_results


def process_results(search_results: list) -> Tuple[dict, int]:
    """
    Prints the search results in an appropriate format and maps them in a dictionary.
    """

    print("Showing the most relevant fetched results.\n")

    result_index = {}

    for i, show in enumerate(search_results):
        # search_results is a list of tv show objects
        # map the shows
        result_index[i + 1] = show

        # print the name, year and country(country given to us in list form)
        if not show["origin_country"]:
            show["origin_country"].append("N/A")

        if not show["first_air_date"]:
            show["first_air_date"] = "N/A"

        print(
            f"{i+1}. {show['name']}, {show['first_air_date'][:4]}, \
{show['origin_country'][0]}"
        )

    return result_index, len(result_index)


def get_users_choice(result_count: int) -> int:
    """
    Get the users' choice of their desired TV show from the fetched results.
    """

    valid_choice = False

    print(
        "Input a number to select the show of your choice. \
Your choice will then be saved in the local database."
    )

    while not valid_choice:
        # giving users the option to go back as well
        if result_count > 1:
            users_choice = int(
                input(f"Enter a no. between 1 and {result_count}, enter 0 to go back: ")
            )

        else:
            users_choice = int(
                input("Enter 1 if you want to select the show, enter 0 to go back: ")
            )

        if users_choice <= result_count:
            valid_choice = True

        return users_choice


def get_show_info(users_choice: int, result_index: dict, tv) -> Tuple[str, int]:

    show_info = result_index[users_choice]

    # we need show id to get the season count
    show_name, show_id = show_info["name"], show_info["id"]

    # searching for the show by using the "tv" object gives us a nested dict
    seasons = tv.details(show_id)["number_of_seasons"]

    return (show_name, seasons)


class Show:
    def __init__(self, name: str, seasons: int):
        self.name = name
        self.seasons = seasons

    def save_to_db(self):
        """
        Save the show to the database.
        """

        query = "INSERT INTO show_data (name, seasons) VALUES (?, ?)"

        with database.ContextManager(db_path) as db:
            try:
                db.cursor.execute(query, [self.name, self.seasons])
                db.conn.commit()
            except sqlite3.Error as e:
                print("error while trying to save show to database", e)

            else:
                print(f"Successfully saved {self.name} to the database!\n")
