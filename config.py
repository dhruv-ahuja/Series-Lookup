from dotenv import load_dotenv
import os
from tmdbv3api import TMDb, TV


# database file
db_file = "serie_db.csv"

# load environment variables
load_dotenv(dotenv_path="./key.env")
api_key = os.getenv("API_KEY")


# initialize tmdb
tmdb = TMDb()
tmdb.api_key = api_key

# config
tmdb.language = "en"
tmdb.debug = True

tv = TV()
