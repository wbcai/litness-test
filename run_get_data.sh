docker run \
-e SPOTIFY_CID=${SPOTIFY_CID} \
-e SPOTIFY_SECRET=${SPOTIFY_SECRET} \
-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
-e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
--mount type=bind,source="$(pwd)"/data,target=/app/data \
litness ./src/get_data.py