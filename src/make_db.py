import os
from os import path
import logging.config
import config
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Float, Integer, String, MetaData


logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('data_pull')

Base = declarative_base()

class Billboard_Spotify(Base):

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

if config.OFFLINE_DB_FLAG:
	# Initiate SQLite DB
	sqlite_engine = sql.create_engine(config.SQLITE_ENGINE)
	Base.metadata.create_all(sqlite_engine)
	logger.info("SQLite database created")
else:
	# set up mysql connection
	mysql_engine = sql.create_engine(config.MYSQL_ENGINE)
	Base.metadata.create_all(mysql_engine)
	logger.info("MySQL database created")
