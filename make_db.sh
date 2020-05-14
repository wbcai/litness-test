docker run -it \
-e MYSQL_HOST=${AVC_MYSQL_HOST} \
-e MYSQL_PORT=${AVC_MYSQL_PORT} \
-e MYSQL_USER=${AVC_MYSQL_USER} \
-e MYSQL_PASSWORD=${AVC_MYSQL_PASSWORD} \
-e DATABASE_NAME=${AVC_DATABASE_NAME} \
--mount type=bind,source="$(pwd)"/data,target=/app/data \
litness ./src/make_db.py 