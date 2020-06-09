#Expected modeling data attributes

SPOTIFY_COLUMNS = ['chart','danceability','energy','key',
					'loudness','mode','speechiness','acousticness',
 					'instrumentalness','liveness','valence','tempo','duration_ms']

# Continuous features (except BPM and Duration) have range between 0 and 1
CONT_FEATURES = ['danceability','energy','speechiness','acousticness',
 					'instrumentalness','liveness','valence']
CONT_MIN = 0
CONT_MAX = 1

# List of expected hot encoded features
HOT_ENCODED_FEATURES = ['key_A', 'key_Ab', 'key_B', 'key_Bb', 'key_C', 'key_D', 'key_Db', 'key_E', 
				'key_Eb', 'key_F', 'key_G', 'key_Gb','mode_major']


EXP_PRECISION = 0.84
EXP_RECALL = 0.77
EXP_AUC = 0.91

TEST_SEARCH = "Rick Astley Never Gonna Give You Up"

EXP_TITLE = "Never Gonna Give You Up"
EXP_ARTIST = "Rick Astley"
EXP_SCORE = 16

EXP_RESULT = {'title': "Never Gonna Give You Up",
				'artist': "Rick Astley",
				'score': 16}