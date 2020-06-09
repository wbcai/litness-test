# Litness Test
## Classifier for Identifying Rap/Hip-Hop Influences from Mainstream Music
### Author: Brian Cai
### QA: Jake Atlas

<!-- toc -->
- [Project charter](#project-charter)
- [Directory structure](#directory-structure)
- [Setting up environment variables](#setting-up-environment-variables)
  * [Spotify environment variables](#spotify-environment-variables)
- [Extracting data from Billboard and Spotify](#Extracting-data-from-Billboard-and-Spotify)
- [Executing model pipeline with Makefile](#Executing-model-pipeline-with-Makefile)
- [Execute each step of model pipeline](#Execute-each-step-of-model-pipeline)
  * [Additional arguments](#Additional-arguments)
- [Running the application](#Running-the-application)
- [Running pipeline and app in Docker](#Running-pipeline-and-app-in-Docker)
  * [Pipeline](#Pipeline)
  * [Application](#Application)
  * [Kill the container](#Kill-the-container) 
- [Backlog](#backlog)

<!-- tocstop -->

## Project charter

**Scenario:**
- We are data science consultants; with our proprietary music information retrieval (MIR) platform, we develop data-driven solutions to tackle problems in the music industry
- Rap/Hip-Hop is perhaps the most dynamic and influential music genres that exists today – it challenges social norms and pushes creativity in music production, and revitalize music across all genres and time periods through sampling 
- A record label has approached us to help them expand their Rap/Hip-Hop division 

**Vision:** Because the label receives hundreds of music files everyday, they are looking for an automated way to prioritize the review of songs with more Rap/Hip-Hop influences 

**Mission:** Use music attributes (e.g., tempo, valence, duration) to predict the probability that a given song is a rap/hip-hop song

**Data sources:**
- List of relevant songs and labels using the [Billboard Chart API](https://github.com/guoguo12/billboard-charts)
  - Charts to obtain songs and genre labels
    - Billboard Hot 100 (Non-Rap/Hip-Hop)
    - Billboard Rap Song (Rap/Hip-Hop)
  - Span: 2000 to 2020, bi-monthly (1st and 15th of every month)
  - Any song that appears in both charts are labeled as Rap/Hip-Hop
- Music attributes from the Spotify API via [Spotipy Library](https://github.com/plamere/spotipy)
  - Attributes: energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms
  - Details of these attributes can be found in the [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

**Success criteria** 
- Model success metric: AUC-ROC curve
- Business success:
  - Ranked list of a given pool of songs, from most likely to have Rap/Hip-Hop influences
  - Provide insights on the most influential attributes for identifying Rap/Hip-Hop songs


    
## Directory structure 

```
├── README.md                         <- You are here
├── app/                              <- Directory for application components
│   ├── docker_build.sh               <- Bash script for creating application Docker image
│   ├── docker_run.sh                 <- Bash script for running app Docker container
│   ├── Dockerfile                    <- Configurations for app Docker image
│   ├── templates/                    <- Directory for app templates
│   │   ├── error.html                <- Error template when app cannot connect to database
│   │   ├── index.html                <- Main application template
│
├── config                            <- Directory for configuration files 
│   ├── flaskconfig.py                <- Configuration of application
│   ├── logging.config                <- Configuration of python logger
│   ├── pipelineconfig.py             <- Configuration of modeling pipeline
│   ├── testconfig.py                 <- Configuration of pipeline validation
│
├── data                              <- Folder that contains data used or generated. 
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/                        <- Notebookes used in development
│
├── src/                              <- Source data for the project 
│   ├── get_data.py                   <- Functions to extract data from APIs
│   ├── predict_score.py              <- Functions to predict probability of a given song
│   ├── train_model.py                <- Functions to train/save predictive model and generate model metrics
│   ├── update_db.py                  <- Functions to create database and save predictions
│
├── test/                             <- Files necessary for running model tests 
│
├── app.py                            <- Flask wrapper for application
├── docker_build.sh                   <- Script to build model pipeline Docker image
├── docker_pipeline.sh                <- Script to execute model pipeline in Docker
├── Dockerfile                        <- Configurations for Docker image
├── env_config                        <- Template to fill in necessary environment variables
├── Makefile                          <- Execution of model pipeline
├── requirements.txt                  <- Python package dependencies 
├── run.py                            <- Script to run each component of the model pipline and make predictions
```

## Setting up environment variables

The environment variables involved in this app are listed in `env_config`. Two environment variables require a Spotify account. Please see section below on instructions for obtaining those variables. After completing the env_config file, set the environment variables following bash commands:

    source env_config
    
Note: Environment variables related to AWS RDS instances are optional. App will by default build a local SQLite database.

### Spotify environment variables

Environment variables `SPOTIFY_CID` and `SPOTIFY_SECRET` are required for obtaining data from the Spotify Web API. You must first create a Spotify user account (Premium or Free). Then go to the [Dashboard](https://developer.spotify.com/dashboard) page at the Spotify Developer website and, if necessary, log in. Accept the latest Developer Terms of Service to complete your account set up.

At the Dashboard, you can now create a new Client ID (i.e., a new app). Once you fill in some general information and accept terms and conditions, you land in the app dashboard. Here you can see your Client ID and Client Secret. The Client ID is the environment variable `SPOTIFY_CID` and the Client Secret is the environment variable `SPOTIFY_SECRET`. For screenshots of these directions, please see `/figures`.

## Extracting data from Billboard and Spotify

To extract the data necessary for the modeling pipeline, run the following command:

    python3 run.py create_dataset

The data will be saved in `data/` and in your designated AWS S3 bucket. Note: it is common to have unsuccessful queries from the Billboard API for certain dates. It is even more common for the Spotify API to not have music attributes for songs from Billboard charts.

## Executing model pipeline with Makefile

Once you extracted and saved the Billboard and Spotify dataset in S3, you can execute the entire model pipeline with the following command:

    make pipeline

Perform unit tests with the following command:

    make validate
    
Reset pipeline (i.e., delete files in `/data` and `/model`):

    make clear

## Execute each step of model pipeline

Execute each step of model pipeline with `run.py` for more configurations.

### Download the extracted dataset from S3:
    
    python3 run.py download_data
    
### Train model, save model object to `/model`, and generate model metrics:

    python3 run.py train_model
   
### Create a database for saving model predictions:

    python3 run.py create_db
   
### Perform unit tests to ensure that all components/configurations are present for making predictions:

    python3 run.py validate
    
### Making and saving predictions

You can make a prediction and save it to your database with the following command:

    python3 run.py predict --search 'Song to predict'

### Additional arguments
- `--engine` or `-e`
  - Specify the use of a local `SQLite` database (default) or `MySQL` database (requires configuration of AWS RDS credentials in `env_config`
  - Applies to `run.py` commands: `create_db`, `validate`, `predict`
- `--uri` or `-u`
  - Specify the use of a engine URI for database; overwrites `--engine` argument
  - Applies to `run.py` commands: `create_db`, `validate`, `predict`
- `--model` or `-m`
  - Specify pathname for model object
  - Applies to `run.py` commands: `train_model`, `predict`

## Running the application

After creating the model and database, you can now run the application:

    python3 app.py

The app is accessible at http://0.0.0.0:5000/ in your browser.

During the model pipeline, if you specified a pathname with the `--model` argument, you must also include the same argument when running the app script (e.g., `python3 app.py --model [model path]`)

By default, the app will use the SQLite database. To use another database URI, save the database URI as environment variable `SQLALCHEMY_DATABASE_URI`.
    
## Running pipeline and app in Docker

### Pipeline

First, make sure Docker Desktop is running. Then to build the image, run the following bash code from the root directory: 

```bash
 docker build -t litness .
```

This command builds the Docker image, with the tag `litness`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

To run the pipeline, execute the following script: 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ litness pipeline \
-e SPOTIFY_CID=${SPOTIFY_CID} \
-e SPOTIFY_SECRET=${SPOTIFY_SECRET} \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
-e AWS_BUCKET=${AWS_BUCKET} 
```
To run unit tests, execute the following scrips:
```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ litness validate \
-e SPOTIFY_CID=${SPOTIFY_CID} \
-e SPOTIFY_SECRET=${SPOTIFY_SECRET} \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
-e AWS_BUCKET=${AWS_BUCKET} 
```

The pipeline and unit tests are orchestrated with the `Makefile`. To add additional arguements (e.g., engine URI, model path), please updated the `Makefile` with arguements from [Additional arguments](#Additional-arguments)

### Application

To build the image, execute the following bash code from the root directory:

```bash
docker build -f app/Dockerfile -t litness .
```
To run the application, execute the following script:

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ \
-e SPOTIFY_CID=${SPOTIFY_CID} \
-e SPOTIFY_SECRET=${SPOTIFY_SECRET} \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
-e AWS_BUCKET=${AWS_BUCKET} \
-p 5000:5000 \
--name test litness app.py
```

### Kill the container 

Once finished with either pipeline or application, you will need to kill the container. To do so: 

```bash
docker kill litness 
```

where `litness` is the name given in the `docker run` command.

## Backlog

**Outline format**:
- **Initiative**
  - **Epic**
    - **Story (size)**
    
- Gather sufficient data to analyze hip-hop trends
  - Obtain list of popular rap and general mainstream songs over the past 20 years
    - Configure program to pull data from Billboard API (M)
    - Obtain monthly top 25 songs from the Billboard Rap Chart and top 50 songs from Billboard Hot 100 Chart at the beginning and middle of each year from 1990 to 2019 (S)
  - Fetch audio attributes of songs
    - Configure program to pull data from Spotify API (M)
    - Pull song attributes of songs from Billboard charts (S)
- Identify ideal model and attributes that can best differentiate music from different eras
  - Perform data exploration and cleansing
     - Evaluate audio attribute differences between rap/hip-hop songs and other mainstream music (M)
     - Understand root cause of missing values, balance categories, etc. (M)
   - Model relationship between songs and their attributes
     - Conduct data transformations and feature engineering (L)
     - Explore various model constructs and evaluate model accuracy (L)
- Derive strategic insights to client based on model results
  - Evaluate model metrics
    - Calculate CV model accuracy (S)
    - Calculate CV r-squared (S)
    - Evaluate feature importance (S)
  - Generate interpretations of model results
    - Evaluate differences between current hip-hop songs compared to past songs (M)
    - Develop stakeholder presentation (L)
- Create tool to take in new songs and predict the era that the song was created
  - Bring model into production
    - Create virtual environment with necessary packages (M)
    - As a user, I want to be able to type in a song and have the model predict the probability that the song is of rap/hip-hop genre (L)
  - Test robustness of model
    - Test edge cases (e.g., Spotify does not have attributes of specific songs)  (L)
    - Evaluate model accuracy (M)

**Icebox**

- Analyze samples used by songs over the years
  - Scrape song sampling data from WhoSampled.com
    - Create program that can retrieve list of samples used by given song (L)
    - Retrieve list of sample used by every song in the top Billboard list (M)
  - Create model features based on the sampled songs
    - Use Spotify API to fetch song attributes (S)
    - Clean / transform data into useable features (M)
  - Evaluate impact of new features
    - Evaluate model metrics (S)
    - Derive new insights based on model results (M)
