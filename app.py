from os import system
import sys
from check_upd import *
from imdb import IMDb
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tabulate import tabulate

#xpath for rotten tomatoes /html/body/div[4]/div[3]/div[5]/section[4]/div

ia = IMDb()

#now I will try to make classes and setup the base for the app

class search:

    
    def welcome(self):
        
        ask_move = input('What would you like to do?\nPress 1 to enter a Netflix show into the local database.\nPress 2 to view the shows stored in the local database.\nPress 3 to check for show updates.\nWrite quit to quit:  ')

        if ask_move == '1':
            pass
        
        elif ask_move == '2':
            print(table().show_db())
            system('pause')
            self.ask_save()
            
        elif ask_move == '3':
            print(check().check_season())
            # system('pause')
            self.ask_save()
        
        elif ask_move == 'quit':
            sys.exit()
        
        else:
            print('\n\nEnter a valid selection!\n\n')
            self.welcome()
    
        
        
    def ask_input(self):
        self.welcome()
        
        
        usr_input = input('Enter the TV Show to search for(please try to be accurate!!): ')
        
        self.show_search = ia.search_movie(usr_input)
        
        print(f'You have entered {usr_input}. Now scouring our online databases.')
        
        
    def results(self):
        self.ask_input()
        print("Showing the most relevant results:")
        print()
        count = 1
        
        entry = self.show_search
        
        
        
        for series in entry:
            yr = 'year'
            
            if series['kind'] == 'tv series' and int(series['year']) > 1990:
                
                print(f'{count}. {series}, {series["year"]}')
                count += 1
                    
        
                    
                
        
                
    
    
    def choose(self):
        self.results()
        select1 = int(input('Select your show from the list, enter a number from 1 to 4 or press 0 to go back to main screen: '))
        
        ent = self.show_search
        
        if 1 <= select1 < 4:
            
            num_map = {
                1 : ent[0] , 2 : ent[1] , 3 : ent[2] , 4 : ent[3]
            }
        
            selection = num_map[select1]
            self.seriesID = selection.movieID
            self.year = selection['year']
        
            print(f"You've chosen {selection}, {self.year}")
            
            self.selection = selection
            return selection
            
            
            
        elif select1 == 0:
            print('Returning you back to the main dialogue.')
            
            return self.ask_save()
            
        
        
        
    def get_seasons(self):
        self.choose()
            
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=2')
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        
        self.query = f"{self.selection} Netflix"

        
        links = []
        
        for site in range(1):
            url = f"http:\\google.com/search?q={self.query}&start="
            driver.get(url)
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            #this is google's current search result link class
            
            search = soup.find_all('div', class_ = 'yuRUbf')

            for h in search:
                links.append(h.a.get('href'))
            
        for site in links:
            show_url = site
            break

        
        parsed = []
        
        #now going to go to the netflix page of the show and grab the season count
        
        for page in range(1):
            url = show_url
            driver.get(url)
            
            soup = BeautifulSoup(driver.page_source, 'lxml')
            search = soup.find_all('span',attrs={'class' : 'test_dur_str'})
            
              
        for res in search:
            parsed.append(res.text[:2])
            print(res.text)
        
        parsed = [i.strip() for i in parsed]
        parsed = [int(i) for i in parsed]
        
        self.season_count = season_count = int()
        for i in parsed:
            season_count = i
            break
        
        print(f'Number of seasons: {season_count} of show: {self.selection}') 
        
        
    def ask_save(self):
        self.get_seasons()
        
        ans = input('Do you want to save the show to the database? Enter "yes" to confirm or "no" to go back to main prompt: ')
        
        if ans == 'no':
            self.ask_save()
            
        else:
            with open('serie_db.txt', 'a+') as file:
                file_pointer = file.read()
                write_data = f'{self.selection}, {self.season_count}  \n'
                
                if write_data in file:
                    print('Show already exists in the database!')
                    
                else:
                    file.write(write_data)
                    print ("Written show and it's season details to the database 😎.") 
                    
        x = input("Enter 'yes' to go back to main page or 'no'/'quit' to quit the program.  ")
        
        if x == 'yes':
            return self.ask_save()
        else:
            return sys.exit()
    
    
    #practicing calling a class method from another class
    # def sup(self):
    #     a = table().func()
    #     return a



class table(search):
    
    # def func(self):
    #     print('Hello')
    
    
    
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
            
            
        # series_db = pandas.DataFrame(series_l, columns = ['Series Name' , 'Season Count'], index = [i for i in range(1, line_count + 1)])
        
        #using tabulate cause it's easy and pretty!
        series_db = tabulate(series_l, headers=['S.no.', 'Show Name' , 'Season Count'], tablefmt='fancy_grid', showindex=[i for i in range(1, line_count+1)])
        
        
        # series_db = series_db.rename()
        return series_db
                    

   
if __name__ == '__main__':
    search().ask_save()
    # close = input('Press ENTER to exit')

# print(search().ask_save())