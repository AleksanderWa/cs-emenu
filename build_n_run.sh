#!/usr/bin/env bash

docker-compose build
docker-compose run web python ./manage.py flush
docker-compose run web python ./manage.py migrate --no-input
docker-compose up -d
docker-compose exec web python ./manage.py seed_db
