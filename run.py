import argparse
import sys
import logging.config
import pickle

from src.update_db import create_db, add_track
from src.predict_score import *

import config

if __name__ == '__main__':

	logging.config.fileConfig(config.LOGGING_CONFIG)
	logger = logging.getLogger('get_data')

	# Add parsers for both creating a database and adding songs to it
	parser = argparse.ArgumentParser(description="Create database / Make predictions")
	parser.add_argument('step', help='Which step to run', choices=['create_db', 'predict'])
	parser.add_argument("--engine", "-e", default = config.SQLITE_ENGINE, 
											help = "SQLAlchemy connection URI for database")
	parser.add_argument("--search", "-s", default = None, help="Song to make prediction")

	args = parser.parse_args()

	if args.step == 'create_db':
		create_db(args.engine)

	if args.step == 'predict':

		if args.search == None:
			logger.warning("No song provided")
			sys.exit()

		model = pickle.load(open(config.MODEL_PATH, "rb" ))

		result = make_prediction(args.search, model)

		print("Litness score of {} by {}: \n {}".format(
						result['title'], result['artist'], result['score']))

		add_track(result, args.engine)