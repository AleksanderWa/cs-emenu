#!/usr/bin/env bash

set -x

docker-compose up --build -d
winpty docker-compose exec web python ./manage.py flush --no-input
winpty docker-compose exec web pytest
