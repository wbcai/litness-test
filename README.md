# Litness Test - Building a Classifier to Identify Rap/Hip-Hop Songs from Mainstream Music
### Author: Brian Cai, QA: Jake Atlas

<!-- toc -->
- [Project charter](#project-charter)
- [Directory structure](#directory-structure)
- [Setting up environment variables](#setting-up-environment-variables)
  * [Spotify environment variables](#spotify-environment-variables)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Connect to NU VPN](#2-connect-to-nu-vpn)
  * [3. Pull data from Billboard and Spotify API](#3-pull-data-from-billboard-and-spotify-api)
  * [4. Establish local SQLite and RDS MySQL databases](#4-establish-local-sqlite-and-rds-mysql-databases)
  * [3. Kill the container](#3-kill-the-container)
- [Backlog](#backlog)

<!-- tocstop -->

## Project charter

**Scenario:**
- We are data science consultants at Spotify; with our proprietary music information retrieval (MIR) platform, we develop data-driven solutions to tackle problems in the music industry
- Hip hop is perhaps the most dynamic and influential music genres that exists today – it challenges social norms and pushes creativity in music production, and revitalize music across all genres and time periods through sampling 
- A record label has approached Spotify to help them expand their rap/hip-hop division 

**Vision:** Because the label receives hundreds of music files everyday, they are looking for an automated way to prioritize the review of songs with rap/hip-hop influences 

**Mission:** Use music attributes (e.g., tempo, valence, duration) to predict the probability that a given song is a rap/hip-hop song

**Data sources:**
- List of relevant hip hop songs obtained using the ![Billboard Chart API](https://github.com/guoguo12/billboard-charts)
- Music attributes gathered from the Spotify API via ![Spotipy Library](https://github.com/plamere/spotipy)


**Success criteria** 
- Model success metric: AUC-ROC curve
- Business success:
  - Ranked list of a given pool of songs, from most likely to have rap/hip-hop influences
  - Provide insights on the most influential attributes for identifying rap/hip-hop songs


    
## Directory structure 

```
├── README.md                         <- You are here
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging.config                <- Configuration of python logger
│
├── data                              <- Folder that contains data used or generated. 
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── requirements.txt                  <- Python package dependencies 
├── get_data.sh                       <- Script to retrieve Billboard and Spotify data in Docker container
├── make_db.sh                        <- Script to make offline SQLite and RDS MySQL databases in Docker container
├── env_config                      <- Template to fill in necessary environment variables

```

## Setting up environment variables

The required environment variables are listed in `env_config`. Note: two environment variables require a Spotify account. Please see section below on instructions for obtaining those variables. After completing the env_config file, set the environment variables in your `~/.bashrc` with the following bash commands:

    echo 'source env_config' >> ~/.bashrc
    source ~/.bashrc 

### Spotify environment variables

Two environment variables, `SPOTIFY_CID` and `SPOTIFY_SECRET`, are required in order to obtain data from the Spotify Web API. To obtain those variables, you must first create/log into a Spotify user account (Premium or Free). Then go to the [Dashboard](https://developer.spotify.com/dashboard) page at the Spotify Developer website and, if necessary, log in. Accept the latest Developer Terms of Service to complete your account set up.

At the Dashboard, you can now create a new Client ID (i.e., a new app). Once you fill in some general information and accept terms and conditions, you land in the app dashboard. Here you can see your Client ID and Client Secret. The Client ID is the environment variable `SPOTIFY_CID` and the Client Secret is the environment variable `SPOTIFY_SECRET`.

## Running the app in Docker 

### 1. Build the image 

To build the image, run the following bash code from the root directory: 

```bash
 docker build -t litness .
```

This command builds the Docker image, with the tag `litness`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Connect to the NU VPN

Connection to the NU VPN is necessary before continuing on. 

### 3. Pull data from Billboard and Spotify API

To obtain song metadata from the Billboard and Spotify API, run the `get_data.sh` script: 

```bash
sh get_data.sh
```
Note: Billboard may fail to pull some Hot 100 charts for certain dates. Spotify Web API also may fail to identify certain songs from the Billboard charts. Both are normal occurances. 

### 4. Establish local SQLite and RDS MySQL databases

To create the databases, run the `make_db.sh` script:

```bash
sh make_db.sh
```

### 5. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

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
