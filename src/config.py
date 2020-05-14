from os import path
import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Billboard charts parameters

START_YEAR = 2010
END_YEAR = 2020

RAPSONG_TOPX = 5
HOT100_TOPX = 5

# Acquire and process config
# MAX_RECORDS_READ = 100
BB_HOT100_LOCATION = path.join(PROJECT_HOME,'data/bb_hot100.json')
BB_RAPSONG_LOCATION = path.join(PROJECT_HOME,'data/bb_rapsong.json')
SPOTIFY_LOCATION = path.join(PROJECT_HOME, 'data/spotify.csv')

# Spotify API keys
SPOTIFY_CID = os.environ.get("SPOTIFY_CID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")

# S3
S3_BUCKET_NAME = 'wbc881bk1'
BB_HOT100_NAME = 'bb_hot100.json'
BB_RAPSONG_NAME = 'bb_rapsong.json'
SPOTIFY_NAME = 'spotify.csv'
