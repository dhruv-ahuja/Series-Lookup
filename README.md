<h1>Series-Lookup </h1>

Check For Show Updates and Get Windows Notifications

<h2>About </h2>

A program made to serve a simple purpose- Add ongoing-shows of your choice to the local database through the app and get the ability to manually check for updates, receiving a Windows toast notification if there's an update. 

<h2>Functionalities</h2>

![image](https://user-images.githubusercontent.com/83733638/134290186-5f7ecc46-86bc-4b61-a245-cf399a0da683.png)

You can search for your shows of choice whose data is scraped through TMDB's API and add the show to a local database(.csv file).

![image](https://user-images.githubusercontent.com/83733638/134289332-b146286a-d6a8-478a-b7e7-a8bb21c307bc.png)

View the stored data in a neat table format.
 

![image](https://user-images.githubusercontent.com/83733638/134290279-d5334cf2-c0fc-47bd-8115-072caf66db59.png)

Receive Windows toast notifications after checking for updates. 

<h2>How to Setup</h2>

1. Clone the repo or download the zip files from [here](https://github.com/good-times-ahead/Series-Lookup/archive/refs/heads/home.zip).
2. Open "config.py" with your code editor of choice and enter your TMDB API key in place of: ```api_key = os.getenv("API_KEY")``` 
3. Create a virtual environment (recommended).
4. Activate the virtual environment if you created one, and run the command "pip install -r requirements.txt" or install using Pipenv.
5. Now that the dependencies have been installed, you can run "app.py" and get started with the app!
