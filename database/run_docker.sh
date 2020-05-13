#export DATABASE_NAME=msia423_db

# docker run -it \
# --env MYSQL_HOST \
# --env MYSQL_PORT \
# --env MYSQL_USER \
# --env MYSQL_PASSWORD \
# --env DATABASE_NAME penny_mysql penny_lane_db.py 

# -p ${MYSQL_PORT}:${MYSQL_PORT} \ 
# echo "sup"
# echo  ${MYSQL_HOST}

docker run -it \
--env MYSQL_HOST \
--env MYSQL_PORT \
--env MYSQL_USER \
--env MYSQL_PASSWORD \
--env DATABASE_NAME \
bb_sp_db bb_sp_db.py 