#!/bin/bash
COMMAND=${1}

# create migrations and migrate
migrate() {
  docker compose run -exec --rm django python manage.py makemigrations
  docker compose run -exec --rm django python manage.py migrate
}

# kill all volumes, networks, images and containers
drop() {
  docker compose down -v
}

# setup project
init() {
  docker compose build
  migrate
  docker compose run -exec --rm django python manage.py createsuperuser
}

start() {
  docker compose up
}

case $COMMAND in
migrate)
  migrate
  ;;
drop)
  drop
  ;;
init)
  init
  ;;
start)
  start
  ;;
*)
  echo 'No action specified!'
  ;;
esac
