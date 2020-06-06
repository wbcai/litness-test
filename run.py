import argparse
import sys
import logging.config
import pickle
import os

from src.predict_score import *
from src.update_db import *
import config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('run')

if __name__ == '__main__':

	# Add parsers for both creating a database and adding songs to it
	parser = argparse.ArgumentParser(description="Create database / Make predictions")
	parser.add_argument('step', help='Which step to run', choices=['get_data', 'create_db', 'predict'])
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

	
	if args.step == 'get_data':
		# Run python script to get data
		os.system('python src/get_data.py')

	if args.step == 'create_db':
		# Create database
		try:
			create_db(engine_uri)
			logger.info("Database created")
		except:
			logger.warning("Database not created")
	
	if args.step == 'predict':
		# Make prediction with song
		if args.search == None:
			logger.warning("No song provided")
			sys.exit()
		model = pickle.load(open(config.MODEL_PATH, "rb" ))
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
