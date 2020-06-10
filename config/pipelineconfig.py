from os import path
import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Billboard charts parameters

START_YEAR = 2000
END_YEAR = 2020

RAPSONG_TOPX = 25
HOT100_TOPX = 40

# Acquire and process config
# MAX_RECORDS_READ = 100
BB_HOT100_LOCATION = path.join(PROJECT_HOME,
	'data/bb_hot100_{}_to_{}.json'.format(START_YEAR, END_YEAR))
BB_RAPSONG_LOCATION = path.join(PROJECT_HOME,
	'data/bb_rapsong_{}_to_{}.json'.format(START_YEAR, END_YEAR))
SPOTIFY_LOCATION = path.join(PROJECT_HOME, 
	'data/spotify_{}_to_{}.csv'.format(START_YEAR, END_YEAR))

# Spotify API keys
SPOTIFY_CID = os.environ.get("SPOTIFY_CID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")

# S3
S3_BUCKET_NAME = 'wbc881bk1'
BB_HOT100_NAME = 'bb_hot100_{}_to_{}.json'.format(START_YEAR, END_YEAR)
BB_RAPSONG_NAME = 'bb_rapsong_{}_to_{}.json'.format(START_YEAR, END_YEAR)
SPOTIFY_NAME = 'spotify_{}_to_{}.csv'.format(START_YEAR, END_YEAR)

# Boolean variable for creation of local database instead of on RDS
OFFLINE_DB_FLAG = True 

# SQLite database
DATABASE_PATH = path.join(PROJECT_HOME, 'data/litness.db')
SQLITE_ENGINE = 'sqlite:////{}'.format(DATABASE_PATH)

# MySQL database
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("AVC_MYSQL_USER")
PASSWORD = os.environ.get("AVC_MYSQL_PASSWORD")
HOST = os.environ.get("AVC_MYSQL_HOST")
PORT = os.environ.get("AVC_MYSQL_PORT")
DATABASE_NAME = os.environ.get("AVC_DATABASE_NAME")
MYSQL_ENGINE = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE_NAME)

# SQLAlchemy database
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is not None:
	pass
else: SQLALCHEMY_DATABASE_URI = SQLITE_ENGINE

#Model
KEY_DICT = {0:'C', 1:'Db', 2: 'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 
			7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
MODE_DICT = {1:'major', 0:'minor'}

SPLIT_SEED = 64
FEATURE_NAMES = ['danceability', 'energy','loudness', 'acousticness', 'speechiness',
				'instrumentalness', 'liveness', 'valence', 'tempo','duration_ms',
				'key_A', 'key_Ab', 'key_B', 'key_Bb', 'key_C', 'key_D', 'key_Db', 'key_E', 
				'key_Eb', 'key_F', 'key_G', 'key_Gb','mode_major']

RFC_PARAMS = {	
			'n_estimators': 200,
			'min_samples_split': 5,
			'min_samples_leaf': 4,
			'max_features': 'auto',
			'max_depth': 10,
			'bootstrap': True,
			'random_state': 64}

MODEL_PATH = path.join(PROJECT_HOME, 'model/random_forest_classifier.pkl')
MODEL_METRICS_PATH = path.join(PROJECT_HOME, 'model/test_metrics.yaml')
FEAT_IMP_PATH = path.join(PROJECT_HOME, 'model/feature_importance.csv')
