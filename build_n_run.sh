#!/usr/bin/env bash

docker-compose up --build -d
winpty docker-compose exec web python ./manage.py flush
winpty docker-compose exec web python ./manage.py migrate --no-input
winpty docker-compose exec web python ./manage.py seed_db
