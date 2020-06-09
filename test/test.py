import pandas as pd
import numpy as np
import pickle
import logging
import yaml
import boto3
import os
from os import path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config.pipelineconfig as config
import config.testconfig as testconfig 
from sqlalchemy.orm import sessionmaker
from src.train_model import prep_data
from src.predict_score import make_prediction
from src.update_db import add_track
from src.train_model import prep_data


logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('__name__')

def validate_training_data():

	""" 
	Ensure all expected columns exist in dataset and have the right values
	Verify that function prep_data correctly hot encoded categorical variables and label
	"""
	
	# Ensure training dataset exists
	if not path.exists(config.SPOTIFY_LOCATION):
		logger.warning("Training dataset does not exist in /data")
	else:
		logger.info("Training dataset exists")
		train_df = pd.read_csv(config.SPOTIFY_LOCATION, index_col = 0)
		train_cols = train_df.columns.tolist()

	# Ensure required column names exists
		column_check = set(testconfig.SPOTIFY_COLUMNS).issubset(set(train_cols))
		if column_check:
			logger.info("All necessary columns exist in training dataset")
		else:
			logger.warning("Training dataset has missing columns")

	# Run function to hot-encode categorical features and split between features and labels
	features, labels = prep_data(train_df, config.FEATURE_NAMES)

	# Validate continuous features that should fall between range 0 and 1
	cont_check = []

	for i in testconfig.CONT_FEATURES:

		max_val = features[i].max()
		min_val = features[i].min()

		logger.debug("{} with {} min and {} max".format(i, min_val, max_val))

		if (max_val <= testconfig.CONT_MAX) & (min_val >= testconfig.CONT_MIN):
			logger.info("{} values fall between expected range of 0 and 1".format(i))
		else:
			cont_check.append(True)
			logger.warning("{} has values that are not between 0 and 1".format(i))


	# Validate hot-encoded categorical features only have value 0, 1
	hot_encode = []

	for i in testconfig.HOT_ENCODED_FEATURES:
		unique_values = features[i].unique().tolist()
		unique_values.sort()

		if unique_values == [0,1]:
			hot_encode.append(False)
		else:
			hot_encode.append(True)
			logger.warning("{} has values that are not 0 and 1".format(i))

	if sum(hot_encode) == 0:
		logger.info("Confirmed that all hot-encoded features have values 0 or 1")
	else:
		logger.warning("Some hot-encoded features do not have values 0 or 1")

	# Validate loudness is 0 or negative

	if features['loudness'].max() > 0:
		logger.warning("Some loudness values are greater than 0; should be 0 or negative")
	else:
		logger.info("Loudness values as expected: 0 or negative")

	# Validate song duration is greater than zero

	if features['duration_ms'].min() > 0:
		logger.info("Duration feature as expected: greater than 0")
	else:
		logger.info("Some durations have values 0 or less")

	# Validate tempo is greater than zero

	if features['tempo'].min() > 0:
		logger.info("Tempo feature as expected: greater than 0")
	else:
		logger.info("Some tempo have values 0 or less")

	# Validate label only has value 0, 1

	label_dist = np.unique(labels).tolist()
	label_dist.sort()

	if label_dist == [0,1]:
		logger.info("Confirmed labels have values 0 or 1")
	else:
		logger.warning("Some labels do not have values 0 or 1")

def check_spotify_credentials():

	""" Ensure Spotify credentials exists/works 
	"""

	client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIFY_CID"), 
															client_secret=os.environ.get("SPOTIFY_SECRET"))

	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

	if (os.environ.get("SPOTIFY_CID") == None) | (os.environ.get("SPOTIFY_SECRET") == None):
		logger.warning("Spotify credentials not set up as environment variables")

	try:
		query = sp.search("Rick+Astley+Never+Gonna+Give+You+Up")
		artist = query['tracks']['items'][0]['artists'][0]['name']
		song = query['tracks']['items'][0]['name']

		print("I LOVE THE SONG {} BY {}".format(song, artist))

		logger.info("Spotify credentials enable API query")
	except:
		logger.warning("Spotify credentials cannot query API")

def check_model_reproducibility(model_path):
	"""
	Confirm that function make_prediction can make prediction with a given input
	Ensure model reproducibility by comparing actual prediction with expected prediction

	"""

	# Ensure model exists

	if not path.exists(model_path):
		logger.warning("Model does not exist")
	else:
		logger.info("Model object file exists")

	# Test model prediction

	try:
		model = pickle.load(open(model_path, "rb" ))
		result = make_prediction(testconfig.TEST_SEARCH, model)
		logger.info("Able to make prediction")
	except:
		logger.warning("Cannot make prediction")

	# Validate model reproducibility

	artist = result['artist']
	title = result['title']
	score = result['score']

	if (artist == testconfig.EXP_ARTIST) & \
		(title == testconfig.EXP_TITLE) & \
		(score == testconfig.EXP_SCORE):
		logger.info("Predictions as expected")
	else:
		logger.warning("Predictions not as expected")

def test_database(sql_path):
	""" Ensure database schema is configured correctly
		Test function add_track for adding additional entries to database
	"""

	try:
		add_track(testconfig.EXP_RESULT, sql_path)
		logger.info("Prediction recorded in database")
	except:
		logger.warning("Cannot add predictions to database")


