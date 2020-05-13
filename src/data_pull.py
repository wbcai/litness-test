import sys
import billboard
from datetime import datetime
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging.config 
import config
import json


logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('data_pull')

def get_billboard_charts(start_year = 1990, end_year = 2020, chart_name = 'rap-song', top_x = 25):
    
    """Fetch tracks from monthly billboard chart
    
    Args: 
        start_year (int): starting year of query
        end_year (int): ending year of query
        chart_name (int): name of billboard chart
        top_x(int): save top x songs from chart
        
    Return:
        query_results (obj): 'list' of artist, song, chart date, and chart name
    
    """
    
    currentmonth = datetime.now().month
    currentyear = datetime.now().year
    
    # Ensure end year is not in the future
    if end_year > currentyear:
        end_year = currentyear
    
    # Ensure start year is not before 1990 (no rap chart)
    if start_year < 1990:
        start_year = 1990
    
    # Create list of monthly dates from start_year to year before end_year
    years = [x for x in range(start_year, end_year)]
    months = ['-01-01','-02-01','-03-01','-04-01','-05-01',  '-06-01', '-07-01','-08-01','-09-01','-10-01','-11-01','-12-01']
    query_dates = [str(y) + d for y in years for d in months]
    
    # Append monthly dates of end_year, accounting for current date
    if end_year < currentyear:
        cur_year_dates = [str(end_year) + d for d in months]
        query_dates.extend(cur_year_dates)
    else:
        cur_year_dates = [str(end_year) + d for d in months[:currentmonth]]
        query_dates.extend(cur_year_dates)
        
    # Fetch chart data from Billboard API

    retry = [] # Unsuccessful queries from first try
    query_results = [] # Results from query
    unsuccessful = [] # Final queries not successful after second try 
    
    
    for qdate in query_dates:
        
        try:
            chart = billboard.ChartData(chart_name, date = qdate)
            results = [[chart[i].artist, chart[i].title, qdate, chart_name] for i in range(0, top_x)]
            query_results.extend(results)
            
            logger.info("{} ... successful query".format(qdate))

        except:
            retry.append(qdate) # if unsuccessfull, add to retry list
            print('{} not found'.format(qdate))
    
    for qdate in retry:
        
        try:
            chart = billboard.ChartData(chart_name, date = qdate)
            results = [[chart[i].artist, chart[i].title, qdate, chart_name] for i in range(0, top_x)]
            query_results.extend(results)
            
            logger.info("{} ... successful query".format(qdate))

        except:
            unsuccessful.append(qdate) # if unsuccessfull, add to retry list
            print('{} not found'.format(qdate))
            
    logger.warning("{} unsuccessful queries".format(len(unsuccessful)))
    
    return query_results


def prep_spotify_query(query_results):
    
    """ Manipulate and concatenate artist and song information based on Spotify API query format. Remove duplicate songs.
    
    Args:
        query_results (obj): 'List' of queries from get_billboard_charts
    
    Return:
        reesults_df (obj): 'DataFrame' of songs with Spotify query column
    
    """
    
    # Remove duplicates
    results_df = pd.DataFrame(query_results, columns = ['artist', 'track', 'date', 'chart'])
    results_df = (results_df.sort_values(by = 'date', ascending = False)
                            .groupby(['artist', 'track']).head(1)
                            .reset_index(drop = True))
    
    
    # Remove parts of the song/artist name that can prevent a successful Spotify query
    
    results_df['artist_q'] = results_df.artist.str.split(' Feat', 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.split('\(Feat', 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.split(' &', 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.split(' ,', 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.split(" Tell'em", 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.split(" Tell 'em", 1).str[0]
    results_df['artist_q'] = results_df.artist_q.str.replace(' X ', ' ')
    results_df['artist_q'] = results_df.artist_q.str.replace(" Co-Starring ", " ")
    results_df['artist_q'] = results_df.artist_q.str.replace("F/", "")
    results_df['artist_q'] = results_df.artist_q.str.replace(' Duet With ', ' ')
    results_df['track_q'] = results_df.track.str.split(" \(", 1).str[0]
    results_df['track_q'] = results_df.track_q.str.split(" Feat", 1).str[0]
    results_df['track_q'] = results_df.track_q.str.split("\(Feat", 1).str[0]
    results_df['track_q'] = results_df.track_q.str.split("/", 1).str[0]
    
    # Create final query column
    results_df['spotify_query'] = (results_df.artist_q + ' ' + results_df.track_q).str.replace(' ', '+')
    
    results_df.drop(['artist_q', 'track_q'], axis = 1, inplace = True)
    
    return results_df

def concat_charts(rap_df, all_df):
    
    """ Create dataframe of songs from hot-100 and rap-song charts. Remove hot-100 songs that are also in rap-song 
    
    """
    
    rap_songs = rap_df.track.values.tolist() # list of songs from rap chart
    
    all_df_no_rap = all_df.loc[~all_df.track.isin(rap_songs), :] # remove rap chart songs from hot-100 chart
    
    concat_df = pd.concat([rap_df, all_df_no_rap]) # combine dataframes
    
    logger.info("{} songs removed from Hot 100".format(len(all_df) - len(all_df_no_rap)))
    
    return concat_df

def get_spotify_metadata(query_df, config.SPOTIFY_CID, config.SPOTIFY_SECRET):
    
    """Obtain song metadata from Spotify API using Spotipy library
    
    Args:
    
        query_df (obj): 'DataFrame' with spotify_query column
        cid (str): CID Spotify credentials
        secret (str): Secret key for Spotify credentials
        
    Return:
    
        results (obj): 'DataFrame' of Spotify metadata
    
    """
    
    
    # Configure spotipy with Spotify credentials
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    
    search_list = query_df['spotify_query'].values.tolist()
    
    query_found = []
    audio_features = []
    not_found = []
    
    # Fetch track metadata from Spotify
    for search in search_list:

        try:
            query = sp.search(search)
            song_id = query['tracks']['items'][0]['id']

            query_found.append(search)
            audio_feature = sp.audio_features(song_id)[0]
            audio_features.append(audio_feature)

        except:
            not_found.append(search)
            print(search, ' not found')
            
    logger.warning("{} songs not found".format(len(not_found)))
            
    spotify_features = pd.DataFrame(audio_features)
    spotify_features['spotify_query'] = query_found
    
    results = query_df.merge(spotify_features, on = 'spotify_query')
    
    return results

def write_records(records, file_location):
    """Persist API response set to file.

    Args:
        records (`:obj:`list` of :obj:`str`): The list of (tweet_id, score) tweet sentiment records.
        file_location (`str`): Location to write file to.

    Returns:
        None
    """

    if not file_location:
        raise FileNotFoundError

    num_records = len(records)
    logger.debug("Writing {} records to {}".format(num_records, file_location))

    with open(file_location, "w+") as output_file:
        json.dump(records, output_file, indent=2)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.error("Failed to upload file to S3", e)
        return False
    return True


if __name__ == "__main__":

	# Get Billboard Hot 100 charts
	try:
		hot100 = get_billboard_charts(chart_name = 'hot-100', top_x = 50)
		hot100_df = prep_spotify_query(hot100)
	except Exception as e:
	    logger.error("Error occured while fetching BB Hot 100.", e)
	    sys.exit(1)

	# Get Billboard Top Rap charts
	try:
		rapsong = get_billboard_charts(chart_name = 'rap-song', top_x = 25)
		rapsong_df = prep_spotify_query(rapsong)
	except Exception as e:
	    logger.error("Error occured while fetching BB Top Rap.", e)
	    sys.exit(1)

	# Merge to single dataframe, removing songs from Hot 100 that are also in Top Rap
	all_df = concat_charts(rapsong_df, hot100_df)

	# Get Spotify metadata
	try:
		spotify_df = get_spotify_metadata(all_df, config.SPOTIFY_CID, config.SPOTIFY_SECRET)
	except Exception as e:
	    logger.error("Error occured while fetching Spotify metadata.", e)
	    sys.exit(1)
	finally:
	    session.close()

	# Export data to local folder
	try:
		write_records(hot100, config.BB_HOT100_LOCATION)
		write_records(rapsong, config.BB_RAPSONG_LOCATION)

		spotify_df.to_csv(config.SPOTIFY_LOCATION)

		logger.info("API records saved")
	except FileNotFoundError:
		logger.error("Please provide a valid file location to persist data.")
		sys.exit(1)

    # Export data to S3
    upload_file(config.BB_HOT100_LOCATION, config.S3_BUCKET_NAME, config.BB_HOT100_NAME)
    upload_file(config.BB_RAPSONG_LOCATION, config.S3_BUCKET_NAME, config.BB_RAPSONG_NAME)
    upload_file(config.SPOTIFY_LOCATION, config.S3_BUCKET_NAME, config.SPOTIFY_NAME)



