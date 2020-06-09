download_data: 
	python3 run.py download_data

train_model:
	python3 run.py train_model

create_db:
	python3 run.py create_db --engine SQLite

pipeline: download_data train_model create_db

validate:
	python3 run.py validate --engine SQLite

run_app:
	python3 app.py

clear:
	rm model/*
	rm data/*
	

.PHONY: pipeline clear