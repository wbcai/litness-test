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
from src.predict_score import make_prediction
from src.update_db import add_track


logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('__name__')

def validate_pipeline(sql_path):
	# Validate training data

	if not path.exists(config.SPOTIFY_LOCATION):
		logger.warning("Training dataset does not exist in /data")
	else:
		logger.info("Training dataset exists")
		train_df = pd.read_csv(config.SPOTIFY_LOCATION)
		train_cols = train_df.columns.tolist()

		column_check = set(testconfig.SPOTIFY_COLUMNS).issubset(set(train_cols))
		if column_check:
			logger.info("All necessary columns exist in training dataset")
		else:
			logger.warning("Training dataset has missing columns")

	# Ensure model exists

	if not path.exists(config.MODEL_PATH):
		logger.warning("Model does not exist")
	else:
		logger.info("Model object file exists")

	# Ensure Spotify credentials exists/works

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

	# Model makes predictions

	try:
		model = pickle.load(open(config.MODEL_PATH, "rb" ))
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

	# Can append predictions to database
	try:
		add_track(result, sql_path)
		logger.info("Prediction recorded in database")
	except:
		logger.info("Cannot add predictions to database")


