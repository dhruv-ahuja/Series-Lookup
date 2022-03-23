import series_lookup.exceptions as exceptions


class Application:
    def __init__(self, tmdb, tv):

        self.tmdb = tmdb
        self.tv = tv

    def __call__(self):

        self.prerun_checks()
        self.welcome()

    def prerun_checks(self):
        """
        Executes all necessary methods before the main application
        logic is run.
        """

        api_key_exists = self.check_api_key()
        if not api_key_exists:
            raise exceptions.NoAPIKeyError(
                "You have not set a TMDB API Key! Please do so before \
using the application."
            )

    def check_api_key(self) -> bool:
        """
        Checks for the presence of the TMDB API Key.
        """

        if not self.tmdb.api_key or "":
            print(self.tmdb.api_key)
            return False

        return True

    def welcome(self) -> int:
        """
        The welcome screen of the app. Shows a list of options to the user, takes user input and feeds the input to other functions in the program.
        """

        input_choices = {0, 1, 2, 3}

        print("Hello, what would you like to do?")
        print("Input 1 to enter a TV show into the local database.")
        print("Input 2 to view the shows stored in the local database")
        print("Input 3 to check for show updates.")
        print("Else, enter 0 to quit the program.")

        valid_input = False

        while not valid_input:
            ask_input = input("Enter your choice: ")

            if int(ask_input) in input_choices:
                valid_input = True
            else:
                print("Invalid choice! Please try again.")

        return int(ask_input)

    def search_for_show(self) -> list:
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
                return None

            search_results = self.tv.search(search_term)

            if not search_results:
                print("Your search did not result in any results, please try again!")

            else:
                valid_input = True

        if len(search_results) > 9:
            search_results = search_results[:8]

        return search_results
