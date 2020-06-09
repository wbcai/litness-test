import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import path
import os
import config.pipelineconfig as config
import pickle
import argparse
import logging.config
import sys

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('__name__')

def query_spotify_id(search):
	""" Query for spotify id, artist, and title
	input:
		search (str): song to search for
		cid (str): Spotify API Client ID
		secret (str): Spotify API Secret ID
	returns:
		result (obj): Dictionary of sotify ID, artist, and title
	"""
	
	search = search.replace(" ", "+")
	
	client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIFY_CID"), 
														client_secret=os.environ.get("SPOTIFY_SECRET"))
	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
	
	query = sp.search(search)
	
	result = {}
	result['id'] = query['tracks']['items'][0]['id']
	result['artist'] = query['tracks']['items'][0]['artists'][0]['name']
	result['title'] = query['tracks']['items'][0]['name']
	
	return result

def get_song_features(song_id):
	""" Query for song metadata
	input:
		song_id (str): song's Spotify ID
		cid (str): Spotify API Client ID
		secret (str): Spotify API Secret ID
	returns:
		result (obj): Dictionary of sotify ID, artist, and title
	"""

	client_credentials_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIFY_CID"), 
														client_secret=os.environ.get("SPOTIFY_SECRET"))

	sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
	
	audio_feature = sp.audio_features(song_id)[0]
	
	return audio_feature

def create_modeling_features(features):
	""" Transform data into compatible format for prediction
	input:
		features (obj): 'Dictionary' of features obtained from Spotify API
	returns:
		model_features_df (obj): 'DataFrame' of features compatible for prediction
	"""
	
	# Get key name, convert to binary feature
	key = config.KEY_DICT[features['key']]
	key_feature_name = "key_" + key
	features.update( {key_feature_name : 1} )
	
	# Add mode_major feature
	features.update({"mode_major": features['mode']})

	# Adjust tempo
	if features['tempo'] < 80:
		features['tempo'] = features['tempo'] * 2
	elif features['tempo'] > 160:
		features['tempo'] = features['tempo'] / 2
	
	# Create dictionary with modeling features
	model_features = {}
	for f in config.FEATURE_NAMES:
		if f in list(features.keys()):
			model_features[f] = features[f]
		else:
			model_features[f] = 0
			
	# Return modeling features as single row DataFrame
	model_features_df = pd.DataFrame([model_features])

	return model_features_df

def make_prediction(search, model):

	""" Make prediction with given query

	inputs:
		search (str): Song to search for
		model (obj): Path of model object for prediction
	returns:
		results (obj): 'Dictionary' of prediction results

	"""

	# Pull Spotify attributes
	try:
		search_result = query_spotify_id(search)
		logger.info("Found {} by {}".format(search_result['title'], 
			search_result['artist']))
	except:
		logger.warning("{} not found. Please try another song".format(search))
		sys.exit()

	features = get_song_features(search_result['id'])

	# Transform data for prediction
	features_df = create_modeling_features(features)

	# Make prediction
	prediction = model.predict_proba(features_df)[0][1]

	# Record results as dictionary
	results = {}

	results['title'] = search_result['title']
	results['artist'] = search_result['artist']
	results['score'] = int(round(prediction * 100, 0))

	return results

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Predict litness score of song query")
	parser.add_argument('--search', '-s', default=None, help='Song to score')

	args = parser.parse_args()

	if args.search == None:
		logger.warning("No song provided")
		sys.exit()

	model = pickle.load(open(config.MODEL_PATH, "rb" ))

	results = make_prediction(args.search, model)

	print("Litness score of {} by {}: \n {}".format(
						results['title'], results['artist'], results['score']))

