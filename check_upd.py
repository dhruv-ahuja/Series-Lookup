from os import name, system
from re import L
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import csv
from win10toast_persist import ToastNotifier
toast = ToastNotifier()


class mklist:
   #find the list of shows stored in the csv as of present moment 
    def read_csv(self):
        data = []
        with open('serie_db.csv', 'r+', newline='') as r:
            reader = csv.reader(r)
            #fields refers to the headings in the 1st line
            fields = next(reader)
            for line in r:
                x,y = line.split(',')
                y = y.strip()
                #packing the show names and seasons into z which then becomes a list so that we can append in 1 go
                *z, = x,y
                data.append(z)
        
        return data
    

class updates(mklist):
    def __init__(self):
        # mklist.__init__(self)
        self.local_data = self.read_csv()
        

    def webscraper(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        scraped_data = list()
        for s in self.local_data:
            name = f'{s[0]} tv show'
            url = driver.get(f'http:\\google.com/search?q={name}')
            soup = BeautifulSoup(driver.page_source, 'lxml')
            parsed = soup.find_all('div', class_ = 'wwUB2c PZPZlf',text=True)
            #assigning the data type to a variable converts it into a bs4 tag type, thus making it possible to directly pull text 
            for _ in parsed:
                scraped = _ 
            scraped = scraped.text
            #this is the symbol the google media section uses to split information
            seasons = scraped.split('‧') [2]
            seasons= int(seasons[1])
            scraped_data.append(seasons)
        
        return scraped_data
        
             
class notify(updates):
    """
    Read the csv file and draw a comparison between the season count stored locally and the one parsed from the internet. If there is a difference, that means that the show has been updated. In that case, send the user a toast notification. 
    """   
    def __init__(self):
        #calling updates as the subclass enables us to call all class variables, neat.
        updates.__init__(self)
        # self.scraped_data = self.webscraper()
    
    
    def compare(self, scraped):
        count = 0
        #data -> [Name, Season Count]
        for num, data in zip(scraped, self.local_data):
            name,s_count = data
            if num > int(s_count):
                
                toast.show_toast('New Season Alert!', f"The show {name} has received a new season!",icon_path='Untitled.ico', duration=None)
                count += 1
                
                #using pandas to read csv file as a dataFrame
                rf = pd.read_csv("serie_db.csv")
                #checks if the dataframe column contains the show name, if so, makes the change as specified.
                rf.loc[rf['Show Name']== name, 'Seasons'] = f'{str(num)}'
                #finally, when you have made required changes, write to the csv file
                rf.to_csv('serie_db.csv', index=False)
        
        toast.show_toast('Overview', f"{count} updates",icon_path='Untitled.ico', duration=None ) if count else toast.show_toast('Overview', f"No updates",icon_path='Untitled.ico', duration=None)
        
       
if __name__ == '__main__':
    # read_csv = mklist().read_csv()
    find_upd = updates().webscraper()
    notify = notify().compare(find_upd)
    