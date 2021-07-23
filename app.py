from os import system
import sys
from check_upd import *
from imdb import IMDb
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv

ia = IMDb()

#now I will try to make classes and setup the base for the app

class app:
    def welcome(self):
        
        ask_move = input('What would you like to do?\nPress 1 to enter a Netflix show into the local database.\nPress 2 to view the shows stored in the local database.\nPress 3 to check for show updates.\nWrite quit to quit:  ')
        
        return ask_move
        

    def ask_input(self):
        
        usr_input = input('Enter the TV Show to search for(please try to be accurate!!): ')
        
        self.show_search = ia.search_movie(usr_input)
        
        print(f'You have entered {usr_input}. Now scouring our online databases.')
        return self.show_search
        
        
    def results(self, show_search):
        
        print("Showing the most relevant results:")
        print()
        count = 1
        
        entry = show_search
        
        for series in entry:
            yr = 'year'
            
            if series['kind'] == 'tv series' and int(series['year']) > 1990:
                
                print(f'{count}. {series}, {series["year"]}')
                count += 1
            
                    
    
    def choose(self, show_search):
        
        select1 = int(input('Select your show from the list, enter a number from 1 to 4 or press 0 to go back to main screen: '))
        
        ent = show_search
        
        if 1 <= select1 < 4:
            
            num_map = {
                1 : ent[0] , 2 : ent[1] , 3 : ent[2] , 4 : ent[3]
            }
        
            selection = num_map[select1]
            seriesID = selection.movieID
            year = selection['year']
        
            print(f"You've chosen {selection}, {year}")
            return selection
            
        elif select1 == 0:
            print('Returning you back to the main dialogue.')
            print()
            print()
            return False


class webscraper(app):
    def __init__(self):
        app.__init__(self)
        
        
    def get_seasons(self, show_name):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=2')
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        query = f'{show_name} Netflix'
        links = []
        url =  f"http:\\google.com/search?q={query}&start="
        driver.get(url)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        search = soup.find_all('div', class_ = 'yuRUbf')
        for h in search:
            links.append(h.a.get('href'))

        show_url = links[0]
        driver.get(show_url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        search2 = soup.find_all('span',attrs={'class' : 'test_dur_str'})
        
        parsed = []
        for page in search2:
            parsed.append(page.text[:2])
        
        parsed = [int(str(i.strip())) for i in parsed]
        self.season_count = season_count = parsed[0]
        
        print(f'Number of seasons: {season_count} of show: {show_name}') 
        return season_count


    def ask_save(self):
        ask = input('Do you want to save the show to the database? Enter "yes" to confirm or "no" to go back to the main prompt: ')
        
        return ask.lower()
    
    
    def write2db(self, show_name, season_count):
        filename = 'serie_db.csv'
        #initializing the titles(will eliminate the need to make rows in the table module BUT we don't need it as it would probably be created each time we run the program and we don't want that):
        fields= ['Show Name', 'Seasons']
        show_info = [show_name, season_count]
        #check to confirm if fields has already been written to the csv file, meaning we have already input data in the csv file earlier
        check = False
        
        with open('serie_db.csv', newline='') as file:
            #delimiter means the separator for the data entries in each line
            r = csv.reader(file, delimiter=',')
            #csv files interpret data as lists(I think)
            for row in r:
                if fields[0] == row[0]:
                    check = True
        
        with open('serie_db.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            #if check is True we only need to write the show details
            if check == True:
                writer.writerow(show_info)
            else:
                #else write the fields data as well, one-time process
                writer.writerow(fields)
                writer.writerow(show_info)
        
        print("Written show and it's season details to the database 😎.")
        print()
        print()
            


class table:
    
    def show_db(self):
        #making line_count to get the number of shows stored in text file
        line_count = 0
    
        with open('serie_db.txt') as file:
            series_list = {}
            
            for line in file:
                showID = ''
                line_data = line.split(',')
                line_count += 1
                
                #we go through this hoop instead of directly equating line_data[1] to an integer because the text file also contains the newline command which gets printed.
                for num in line_data[1]:
                    if num.isnumeric():
                        showID += str(num)
                        
                line_data[1] = int(showID)
                
                series_list[line_data[0]] = line_data[1]
            
            
            #now, to remove duplicates
        series_list = [(l, m) for l, m in series_list.items()]
        series_l = []
        
        for entry in series_list:
            if entry not in series_l:
                series_l.append(entry)
            

        #using tabulate cause it's easy and pretty!
        series_db = tabulate(series_l, headers=['S.no.', 'Show Name' , 'Season Count'], tablefmt='fancy_grid', showindex=range(1, line_count+1))
        
        
        print(series_db)
                    
def main():
    launch = app().welcome()
    
    if launch == '1':
        show_search = app().ask_input()
        results = app().results(show_search)
        user_choice = app().choose(show_search)
        if user_choice == False:
            launch
        else:
            get_seasons = webscraper().get_seasons(user_choice)
            ask_save = webscraper().ask_save()
            if ask_save == 'no':
                launch
            write_data = webscraper().write2db(user_choice, get_seasons)
            
        
    
    elif launch == '2':
        show_db = table().show_db()
        system('pause')
        print()
        # write_data = app().ask_save()
        launch
    
    elif launch == '3':
        pass
    
    elif launch == 'quit':
        sys.exit()
    
    else:
      print('\n\nEnter a valid selection!\n\n')  
      return False
    
   
if __name__ == '__main__':
    
    while True:
        main()
    