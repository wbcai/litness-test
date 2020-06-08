download_data: 
	python3 run.py download_data

train_model:
	python3 run.py train_model

create_db:
	python3 run.py create_db --engine MySQL

validate:
	python3 run.py validate --engine MySQL

pipeline: download_data train_model create_db validate

clear:
	rm model/*
	rm data/*
	

.PHONY: pipeline clear