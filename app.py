import traceback
from flask import render_template, request, redirect, url_for, flash
import logging.config
from flask import Flask
from src.predict_score import *
from src.update_db import Litness
from flask_sqlalchemy import SQLAlchemy
import config.pipelineconfig as config
import pickle

# Create argparser for user to specify model object
parser = argparse.ArgumentParser(description="Run Flask app")
parser.add_argument("--model", "-m", default = None, help="Path for model object")
args = parser.parse_args()

if args.model is not None:
	model_path = args.model
else:
	model_path = config.MODEL_PATH


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

# Import pre-trained model
try:
	model = pickle.load(open(model_path, "rb" ))
	logging.debug("Model loaded from %s", model_path)
except:
	logging.warning("Cannot load model from $s", model_path)

error = None

@app.route('/')
def index():
	"""Main view that lists songs in the database.

	Create view into index page that uses data queried from Track database and
	inserts it into the msiapp/templates/index.html template.

	Returns: rendered html template

	"""

	global error

	try:
		tracks = db.session.query(Litness).order_by(Litness.id.desc()).limit(app.config["MAX_ROWS_SHOW"]).all()
		logger.debug("Index page accessed")
		return render_template('index.html', tracks=tracks, error = error)
	except:
		traceback.print_exc()
		logger.warning("Not able to display tracks, error page returned")
		return render_template('error.html')

@app.route('/add', methods=['POST'])
def add_prediction():
	"""View that process a POST with new song input

	:return: redirect to index page
	"""

	global error 

	search = request.form['search']
	logger.info("%s captured from search", search)
	
	try:
		prediction = make_prediction(search, model)
		logger.info("Prediction made: {}".format(prediction['score']))
		entry = Litness(title=prediction['title'], artist=prediction['artist'], score=prediction['score'])
		error = None
	except:
		error = "Cannot score that song, please try another"
		return redirect(url_for('index'))
	
	if error == None:
		try:    
			db.session.add(entry)
			db.session.commit()
			logger.info("New song added: %s by %s", prediction['title'], prediction['artist'])
			return redirect(url_for('index'))
		except:
			logger.warning("Not able to display tracks, error page returned")
			return render_template('error.html')


if __name__ == '__main__':
	app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
