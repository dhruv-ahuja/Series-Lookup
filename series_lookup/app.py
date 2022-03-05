class Application:
    def __init__(self):
        self.welcome()

    def welcome(self):
        """
        The welcome screen of the app. Shows a list of options to the user, takes user input and feeds the input to other functions in the program.
        """

        input_choices = {"0", "1", "2", "3"}

        print("Hello, what would you like to do?")
        print("Input 1 to enter a TV show into the local database.")
        print("Input 2 to view the shows stored in the local database")
        print("Input 3 to check for show updates.")
        print("Else, enter 0 to quit the program.")

        valid_input = False

        while not valid_input:
            ask_input = input("Enter your choice: ")

            if ask_input in input_choices:
                valid_input = True
            else:
                print("Invalid choice! Please try again.")

        return ask_input
