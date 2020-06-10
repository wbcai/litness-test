from os import path
import os

# MySQL database
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("AVC_MYSQL_USER")
PASSWORD = os.environ.get("AVC_MYSQL_PASSWORD")
HOST = os.environ.get("AVC_MYSQL_HOST")
PORT = os.environ.get("AVC_MYSQL_PORT")
DATABASE_NAME = os.environ.get("AVC_DATABASE_NAME")
MYSQL_ENGINE = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE_NAME)

print(MYSQL_ENGINE)