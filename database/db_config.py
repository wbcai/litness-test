from os import path
import os

# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Offline database
DATABASE_PATH = path.join(PROJECT_HOME, 'data/billboard_spotify.db')
SQLITE_ENGINE = 'sqlite:////{}'.format(DATABASE_PATH)
#SQLALCHEMY_TRACK_MODIFICATIONS = True
#SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# RDS database 
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST")
PORT = os.environ.get("MYSQL_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
MYSQL_ENGINE = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE_NAME)