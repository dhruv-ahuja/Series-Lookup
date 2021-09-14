import os
import sys
from check_upd import *
from imdb import IMDb
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv

ia = IMDb()

# now I will try to make classes and setup the base for the app


class App:
    def __init__(self) -> None:
        self.check_for_csv()

    def check_for_csv(self):
        """Creates a CSV file to store data if it does not yet exist."""

        path = ".\serie_db.csv"

        try:
            if not os.path.exists(path):
                print("Creating database file (first time user)")
                print("................................")
                with open("serie_db.csv", "w") as db:
                    pass

                print("Created database file")
                print()

        except OSError as e:
            print(
                "Unable to create Database file to store information, please check your permissions!"
            )

    def welcome(self):
        """The welcome screen of the app. Shows a list of options to the user, takes user input and feeds the input to other functions in the program."""

        print("What would you like to do?")
        print("Input 1 to enter a Netflix show into the local database.")
        print("Input 2 to view the shows stored in the local database")
        print("Input 3 to check for show updates.")
        ask_move = input("Else, input 'quit' to quit the program: ")

        return ask_move

    def ask_input(self):

        usr_input = input(
            "Enter the TV Show to search for(please try to be accurate!!): "
        )

        self.show_search = ia.search_movie(usr_input)

        print(f"You have entered {usr_input}. Now scouring our online databases.")
        return self.show_search

    def results(self, show_search):

        print("Showing the most relevant results:")
        print()
        count = 1

        entry = show_search

        for series in entry:
            yr = "year"

            if series["kind"] == "tv series" and int(series["year"]) > 1990:

                print(f'{count}. {series}, {series["year"]}')
                count += 1

    def choose(self, show_search):
        # need to check if the user has made a valid choice or not, if not, keep asking them
        valid_choice = False

        while not valid_choice:
            select1 = int(
                input(
                    "Select your show from the list, enter a number from 1 to 4 or press 0 to go back to main screen: "
                )
            )

            ent = show_search

            if 1 <= select1 < 4:
                num_map = {1: ent[0], 2: ent[1], 3: ent[2], 4: ent[3]}

                selection = num_map[select1]
                seriesID = selection.movieID
                year = selection["year"]

                print(f"You've chosen {selection}, {year}")

                valid_choice = True
                return selection

            elif select1 == 0:
                print("Returning you back to the main dialogue.")
                print()
                print()
                valid_choice = True
                return False

            elif select1 > 4:
                print("Please enter a valid number!")
                print()


class Webscraper:
    def get_seasons(self, show_name):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("log-level=2")

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )

        query = f"{show_name} Netflix"
        links = []
        url = f"http:\\google.com/search?q={query}&start="
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "lxml")
        search = soup.find_all("div", class_="yuRUbf")
        for h in search:
            links.append(h.a.get("href"))

        show_url = links[0]
        driver.get(show_url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        search2 = soup.find_all("span", attrs={"class": "test_dur_str"})

        parsed = []
        for page in search2:
            parsed.append(page.text[:2])

        parsed = [int(str(i.strip())) for i in parsed]
        self.season_count = season_count = parsed[0]

        print(f"Number of seasons: {season_count} of show: {show_name}")
        return season_count

    def ask_save(self):
        ask = input(
            'Do you want to save the show to the database? Enter "yes" to confirm or "no" to go back to the main prompt: '
        )

        return ask.lower()

    def write2db(self, show_name, season_count):
        filename = "serie_db.csv"
        # initializing the titles:
        fields = ["Show Name", "Seasons"]
        show_info = [show_name, season_count]
        # check to confirm if fields has already been written to the csv file, meaning we have already input data in the csv file earlier
        check, is_data_present = False, False

        with open("serie_db.csv", newline="") as file:
            # delimiter means the separator for the data entries in each line
            r = csv.reader(file, delimiter=",")
            # csv files interpret data as lists(I think)
            for row in r:
                if fields[0] == row[0]:
                    check = True
                # if the show data is already in the csv, trigger
                if row[0] == str(show_info[0]):
                    is_data_present = True

        with open("serie_db.csv", "a+", newline="") as file:
            writer = csv.writer(file)

            # if check is True we only need to write the show details
            if check == True and is_data_present == False:
                writer.writerow(show_info)

                print("Written show and it's season details to the database 😎.")

            elif check == False and is_data_present == False:
                # else write the fields data as well, one-time process
                writer.writerow(fields)
                writer.writerow(show_info)

                print("Written show and it's season details to the database 😎.")

            if is_data_present == True:
                print()
                print(
                    "The show already exists in the database!",
                    "Going back to the main screen now.",
                )
                system("pause")

        print()


class table:
    def getdata(self):

        csv_size = os.path.getsize("serie_db.csv")

        if not csv_size:

            return False

        with open("serie_db.csv", newline="") as r:
            reader = csv.reader(r, delimiter=",")
            # reading the 1st line to get the fields, stored as a list
            fields = next(reader)
            fields = tuple(fields)
            data = []

            for _ in reader:
                data.append(_)

        return data, fields

    def make_table(self, data, fields):

        table = tabulate(
            data,
            headers=["S. No.", f"{fields[0]}", f"{fields[1]}"],
            tablefmt="fancy_grid",
            showindex=range(1, len(data) + 1),
        )

        print(table)


if __name__ == "__main__":
    """Using a while loop here to be able to run the program indefinitely until the user decides to quit."""

    app_persist = True

    while app_persist:

        app = App()
        init = app.welcome()

        if init == "1":
            show_search = App().ask_input()
            results = App().results(show_search)
            user_choice = App().choose(show_search)

            if user_choice == False:
                print("Going back to the main screen.")
                init

            else:
                get_seasons = Webscraper().get_seasons(user_choice)
                ask_save = Webscraper().ask_save()

                if ask_save == "no":
                    break
                    # app should start again at this point, as of now it just terminates
                write_data = Webscraper().write2db(user_choice, get_seasons)

                init

        elif init == "2":
            getdata = table().getdata()

            if getdata is False:
                print(
                    "No shows entered in the database! Please save a show first before accessing this option."
                )
                system("pause")
                print()
                init

            else:
                re_data = table().make_table(getdata[0], getdata[1])

                system("pause")
                print()
                init
                # ask_for_input = True

        elif init == "3":
            find_upd = updates().webscraper()
            update_db = notify().compare(find_upd)

            system("pause")
            print()
            init

        elif init == "quit":
            app_persist = False

        else:
            print("Enter a valid selection!\n")
