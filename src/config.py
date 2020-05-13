from os import path
import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# App config
APP_NAME = "isthisrap"
DEBUG = True

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Database connection config
DATABASE_PATH = path.join(PROJECT_HOME, 'data/billboard_spotify.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# Acquire and process config
# MAX_RECORDS_READ = 100
BB_HOT100_LOCATION = path.join(PROJECT_HOME,'data/bb_hot100.json')
BB_RAPSONG_LOCATION = path.join(PROJECT_HOME,'data/bb_rapsong.json')
SPOTIFY_LOCATION = path.join(PROJECT_HOME, 'data/spotify.csv')

# Spotify API keys
SPOTIFY_CID = os.environ.get("spotify_cid")
SPOTIFY_SECRET = os.environ.get("spotify_secret")

# S3
S3_BUCKET_NAME = 'wbc881bk1'
BB_HOT100_NAME = 'bb_hot100.json'
BB_RAPSONG_NAME = 'bb_rapsong.json'
SPOTIFY_NAME = 'spotify.csv'
