import os
from os import path
import logging.config
import config
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Float, Integer, String, MetaData


logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('make_db')

Base = declarative_base()

class Litness(Base):

	"""Create a data model for the database to be set up for capturing songs from Billboard charts """

	__tablename__ = 'litness'
	
	id = Column(Integer(), primary_key=True)
	title = Column(String(100), unique=False, nullable=False)
	artist = Column(String(100), unique=False, nullable=False)
	score = Column(Integer(), unique=False, nullable=False)

	def __repr__(self):
		song_repr = "<Chart(Title='%s', Artist='%s', Litness Score='%s')>"
		return song_repr % (self.title, self.artist, self.score)

if __name__ == "__main__":

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
