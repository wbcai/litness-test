import os
import config.pipelineconfig

DEBUG = True
LOGGING_CONFIG = "config/logging.conf"
PORT = 5000
APP_NAME = "litness-test"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 10

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
if SQLALCHEMY_DATABASE_URI is not None:
	pass
else: SQLALCHEMY_DATABASE_URI = config.pipelineconfig.SQLITE_ENGINE