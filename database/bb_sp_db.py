import os
from os import path
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Float, Integer, String, MetaData


# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# Logging
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging.conf')

# Offline database
DATABASE_PATH = path.join(PROJECT_HOME, 'data/billboard_spotify.db')
SQLITE_ENGINE = 'sqlite:////{}'.format(DATABASE_PATH)

# RDS database 
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST")
PORT = os.environ.get("MYSQL_PORT")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
MYSQL_ENGINE = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE_NAME)


Base = declarative_base()

class Chart(Base):

    """Create a data model for the database to be set up for capturing songs from Billboard charts """

    __tablename__ = 'chart'
    
    id = Column(Integer(), primary_key=True)
    song = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    chart = Column(String(100), unique=False, nullable=False)
    date = Column(String(100), unique=False, nullable=False)
    danceability = Column(Float(), unique=False, nullable=False)
    energy = Column(Float(), unique=False, nullable=False)
    key = Column(String(200), unique=False, nullable=False)
    loudness = Column(Float(), unique=False, nullable=False)
    mode = Column(String(200), unique=False, nullable=False)
    speechiness = Column(Float(), unique=False, nullable=False)
    acousticness = Column(Float(), unique=False, nullable=False)
    instrumentalness = Column(Float(), unique=False, nullable=False)
    liveness  = Column(Float(), unique=False, nullable=False)
    valence = Column(Float(), unique=False, nullable=False)
    tempo  = Column(Float(), unique=False, nullable=False)
    time_signature = Column(Integer(), unique=False, nullable=False)

    def __repr__(self):
        song_repr = "<Chart(song='%s', artist='%s', chart='%s', date='%s')>"
        return song_repr % (self.song, self.artist, self.chart, self.date)


# Initiate SQLite DB
sqlite_engine = sql.create_engine(SQLITE_ENGINE)
Base.metadata.create_all(sqlite_engine)

# set up mysql connection
mysql_engine = sql.create_engine(MYSQL_ENGINE)
Base.metadata.create_all(mysql_engine)
