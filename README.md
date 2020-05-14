# Litness Test - Building a Classifier to Identify Rap/Hip-Hop Songs from Mainstream Music
### Author: Brian Cai, QA: Jake Atlas

<!-- toc -->
- [Project charter](#project-charter)
- [Directory structure](#directory-structure)
- [Intialize the database](#initialize-the-database)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
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
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Initialize the database


## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.

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
    - As a user, I want to be able to type in a hip hop song and have the model predict what era the song came from (L)
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
