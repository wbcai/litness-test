import os

DEBUG = True
LOGGING_CONFIG = "config/logging.conf"
PORT = 5000
APP_NAME = "litness-test"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100

# Connection string
DB_HOST = os.environ.get('AVC_MYSQL_HOST')
DB_PORT = os.environ.get('AVC_MYSQL_PORT')
DB_USER = os.environ.get('AVC_MYSQL_USER')
DB_PW = os.environ.get('AVC_MYSQL_PASSWORD')
DATABASE = os.environ.get('AVC_DATABASE_NAME')
DB_DIALECT = 'mysql+pymysql'
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/litness.db'

# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
# if SQLALCHEMY_DATABASE_URI is not None:
#     pass
# elif DB_HOST is None:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///data/litness.db'
# else:
#     SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}' \
#     		.format(dialect=DB_DIALECT, user=DB_USER,pw=DB_PW, host=DB_HOST, 
#     			port=DB_PORT, db=DATABASE)