docker run -it \
-e MYSQL_HOST=msia423-bcai.cvomuhyyfy7x.us-east-2.rds.amazonaws.com \
-e MYSQL_PORT=3306 \
-e MYSQL_USER=${AVC_MYSQL_USER} \
-e MYSQL_PASSWORD=${AVC_MYSQL_PASSWORD} \
-e DATABASE_NAME=db1 \
--mount type=bind,source="$(pwd)"/data,target=/app/data \
makedb bb_sp_db.py 