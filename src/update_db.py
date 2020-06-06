import argparse
import logging.config
import yaml
import os

import logging.config
import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Float, Integer, String, MetaData

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

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

def create_db(sql_path):
	"""Creates a database with the data model given by obj:`apps.models.Track`

	Args:
		args: Argparse args - should include args.title, args.artist, args.score

	Returns: None

	"""

	engine = sqlalchemy.create_engine(sql_path)

	Base.metadata.create_all(engine)

	Session = sessionmaker(bind=engine)
	session = Session()

	session.commit()
	logger.info("Database created")
	session.close()

def add_track(result, sql_path):
	"""Seeds an existing database with additional songs.

	Args:
		args: Argparse args - should include args.title, args.artist
		score (int): prediction score

	Returns:None

	"""

	engine = sqlalchemy.create_engine(sql_path)

	Session = sessionmaker(bind=engine)
	session = Session()

	track = Litness(artist=result['artist'], title=result['title'], score=result['score'])
	session.add(track)
	session.commit()
	logger.info("{} by {} with score {} added to database" \
			.format(result['title'], result['artist'], result['score']))

