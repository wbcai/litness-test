import pandas as pd
import numpy as np
import pickle
import logging
import yaml
import boto3
from os import path

import config.pipelineconfig as config

from sklearn.preprocessing import LabelEncoder 
from sklearn.preprocessing import OneHotEncoder 
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('__name__')

def download_data(bucket_name, object_name, save_path):
	""" Download model data from S3 bucket
	input:
		bucket_name (str)
		object_name (str)
		save_path (str)
	"""

	s3 = boto3.client('s3')
	try:
		s3.download_file(bucket_name, object_name, save_path)
	except:
		logger.warning("Cannot download data from S3")

	return None

def prep_data(spotify_df, feature_names):

	""" Hot encode categorical variables, create features and labels DataFrame

	input:
		spotify_df (obj): DataFrame of Spotify metadata
		features (obj): List of features to be used for model

	output:
		model_df (obj): DataFrame of features
		labels_df (obj): Series of labels (1 for rap-song, 0 for Hot 100)
	"""
	# Convert key and mode intergers into names
	spotify_df['key_name'] = spotify_df['key'].map(config.KEY_DICT)
	spotify_df['mode_name'] = spotify_df['mode'].map(config.MODE_DICT)

	# Hot encode categorical variables and response
	spotify_df = pd.get_dummies(spotify_df, columns=["chart", "key_name", 'mode_name'],
											prefix=["chart", "key", "mode"] )
	# Create features and labels DataFrame
	features = spotify_df.loc[:, feature_names]
	labels = np.array(spotify_df['chart_rap-song'])

	logger.debug("Features and labels created")

	return features, labels

def test_model(features, labels, split_seed, **kwargs):

	""" Fit model on training dataset then calculate/save model metrics for testing dataset
	input:
		features (obj): DataFrame of features
		lable (obj): Series of labels
		split_seed (int): seed for data split into train and test
		**kwargs (obj): Keyword arguments for sklearn.ensemble.RandomForestClassifier
	output:
		metrics (obj): Dictionary of metrics
	"""

	# Split data into train and test
	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, 
																			test_size = 0.25, random_state = split_seed)
	
	# Fit model with training data
	model = RandomForestClassifier(**kwargs)
	model.fit(train_features, train_labels)
	logger.debug("Model fit with training data")
	# Predict probabilities with testing data
	test_predictions = model.predict(test_features)
	test_probs = model.predict_proba(test_features)[:, 1]

	# Obtain model metrics
	metrics = {}

	metrics['baseline_recall'] = round(recall_score(test_labels, 
									 [1 for _ in range(len(test_labels))]), 2).tolist()
	metrics['baseline_precision'] = round(precision_score(test_labels, 
									  [1 for _ in range(len(test_labels))]),2).tolist()
	metrics['baseline_roc'] = 0.5

	metrics['test_recall'] = round(recall_score(test_labels, test_predictions),2).tolist()
	metrics['test_precision'] = round(precision_score(test_labels, test_predictions),2).tolist()
	metrics['test_roc'] = round(roc_auc_score(test_labels, test_probs),2).tolist()
	logger.debug("Model metrics calculated")
	return metrics


def download_training_data():

	# Import modeling data; download from S3 bucket if not in data folder
	if not path.exists(config.SPOTIFY_LOCATION):
		logger.debug("Downloading modeling data from S3 bucket")
		download_data(config.S3_BUCKET_NAME, config.SPOTIFY_NAME, config.SPOTIFY_LOCATION)
	else:
		logger.info("Training data already exists")

def create_model(model_path):

	try:
		spotify_df = pd.read_csv(config.SPOTIFY_LOCATION)
	except:
		logger.warning("Training data does not exist")

	# Hot encode categorical variables and response
	features, labels = prep_data(spotify_df, config.FEATURE_NAMES)

	# Obtain metrics from testing data
	metrics = test_model(features, labels, config.SPLIT_SEED, **config.RFC_PARAMS)

	try:
		with open(config.MODEL_METRICS_PATH, "w") as file:
			yaml.dump(metrics, file)
		logger.info("Model metrics saved as %s", config.MODEL_METRICS_PATH)
	except:
		logger.warning("Model metrics not saved")


	# Train model on full dataset and save to model folder
	rfc_model = RandomForestClassifier(**config.RFC_PARAMS)
	rfc_model.fit(features, labels)

	# If model path was not provided, use default config path
	if model_path is None:
		logger.warning("Model path not provided")
		
	# Save model	
	try:
		with open(model_path, "wb") as f:
				pickle.dump(rfc_model, f)
		logger.info("Trained model object saved as %s", model_path)
	except:
		logger.warning("Trained model not saved")

	# Create feature importance dataframe and save to model folder
	importance = rfc_model.feature_importances_.tolist()
	feat_imp_df = pd.DataFrame({'feature': config.FEATURE_NAMES, 
						'gini_importance': importance})

	try:
		feat_imp_df.to_csv(config.FEAT_IMP_PATH, index = False)
		logger.info("Feature importance saved as %s", config.FEAT_IMP_PATH)
	except:
		logger.warning("Feature importance not saved")

