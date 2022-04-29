from dotenv import load_dotenv
from tmdbv3api import TMDb, TV


import os


load_dotenv()

db_path = "serie_db.db"
api_key = os.getenv("API_KEY")

# initialize tmdb
tmdb = TMDb()
tmdb.api_key = api_key
tmdb.language = "en"
tmdb.debug = True

# initialize the tv object to be used later
tv = TV()
