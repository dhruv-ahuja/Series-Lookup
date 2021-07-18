from os import name, system
from imdb import IMDb
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from win10toast_persist import ToastNotifier
toast = ToastNotifier()


class info:
    #setting up the data dictionary that contains all tv shows and their season count stored locally
    def __init__(self, data = dict()):
        self.data = data
        

        with open('serie_db.txt') as file:
            for line in file:
                
                show,season = line.split(',')
                show,season = show.rstrip(), season.rstrip()
                
                data[show] = int(season)
                
                
    
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=2')
        self.chrome_options = chrome_options
        
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.driver = driver
    
    
    
    def __getdata__(self, key):
        try:
            return self.data[key]
            
        except KeyError:
            print('Show not in the list.')
        
    
    def getdata(self, key):
        return self.__getdata__(key)
        
    
    def findlinks(self):
        len_count = len(self.data)
        show_links = []
        
        
        for link in self.data:
            query = f'{link} netflix'
            url = f"http:\\google.com/search?q={query}&start="
            self.driver.get(url)
            
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            search = soup.find_all('div', class_ = 'yuRUbf')
            
            
            for link in search:
                show_links.append(link.a.get('href'))
                break
        return show_links 
        #now we have all the links ready in show_links variable 
        
    def findcount(self): 
        parsed = list()
        show_links = self.findlinks()
        
        for link in show_links:
            self.driver.get(link)

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            search = soup.find_all('span',attrs={'class' : 'test_dur_str'})

            for res in search:
                parsed.append(res.text[:2])
        
        parsed = [i.strip() for i in parsed]
        parsed = [int(i) for i in parsed]
        
        return parsed

    def getparsed(self):
        return self.findcount()


class check(info):
    def __init__(self):
        info.__init__(self)
        parsed = self.getparsed()
        self.parsed = parsed    
    
    
    def check_season(self):
       
       
        
        for i, j, k in zip(self.data.values(), self.parsed, self.data.keys()):
            newdict = {}
            if j > i:
                
                x = toast.show_toast('New Season Alert!', f"The show {k} has received a new season!",icon_path='Untitled.ico', duration=None )
                
                #replace the existing value with a new value
                with open('serie_db.txt', 'r+') as file:
                    # file.read()
                    for line in file:
                        
                        name, number = line.split(',')
                        if name == k:
                            newdict[name] = f'{j}  \n'
                            
                        else:
                            newdict[name] = f'{number}'
                
            
                with open('serie_db.txt', 'w+') as file:
                    for (name, num) in newdict.items():
                        file.write(f'{name}, {num}')
                
                return x
        toast.show_toast('No Updates Found', 'No updates found for the shows',icon_path='Untitled.ico', duration=None)
        
        system('pause')
        return ''
                
              
    
        
            
# if __name__ == '__main__':
#     pass          
            
