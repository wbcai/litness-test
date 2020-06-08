import argparse
import sys
import logging.config
import pickle
import os

from src.get_data import create_dataset
from src.train_model import download_training_data, create_model
from src.predict_score import make_prediction
from src.update_db import create_db, add_track
from test.test import validate_pipeline
import config.pipelineconfig as config

logging.config.fileConfig(config.LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger('__name__')

if __name__ == '__main__':

	# Add parsers for both creating a database and adding songs to it
	parser = argparse.ArgumentParser(description="Create database / Make predictions")
	parser.add_argument('step', help='Which step to run', choices=['create_dataset', 'download_data', 'train_model', 'create_db', 'predict', 'validate'])
	parser.add_argument("--uri", "-u", default = None, help = "Specify SQLAlchemy connection URI for database")
	parser.add_argument("--search", "-s", default = None, help="Song to make prediction")
	parser.add_argument("--engine", "-e", default = "SQLite", 
									help="Specify MySQL or SQLite; connection URI based on environment variables")

	args = parser.parse_args()

	# Determine engine URI based on arguments
	if args.uri:
		engine_uri = args.uri
	else:
		if args.engine == "SQLite":
			engine_uri = config.SQLITE_ENGINE
		else:
			engine_uri = config.MYSQL_ENGINE

	
	if args.step == 'create_dataset':
		# Gather data from Billboard and Spotify API
		create_dataset()

	if args.step == 'download_data':
		# Download training data from S3
		download_training_data()

	if args.step == 'train_model':
		# Train model and generate model metrics
		create_model()

	if args.step == 'create_db':
		#Create database
		try:
			create_db(engine_uri)
		except:
			logger.warning("Database not created")
	
	if args.step == 'predict':
		# Make prediction with song
		if args.search == None:
			logger.warning("No song provided")
			sys.exit()
		try:
			model = pickle.load(open(config.MODEL_PATH, "rb" ))
		except:
			logger.warning("Model does not exist")
		try:
			result = make_prediction(args.search, model)
			print("Litness score of {} by {}: \n {}".format(
						result['title'], result['artist'], result['score']))
		except:
			logger.warning("Cannot make prediction with song; try another")
		# Save prediction to database
		try:
			add_track(result, engine_uri)
			logger.info("Prediction recorded in database")
		except:
			logger.warning("Prediction not recorded in database")

	if args.step == 'validate':
		# Validate pipeline
		validate_pipeline(engine_uri)

