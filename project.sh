#!/bin/bash
COMMAND=${1}

migrate() {
  docker compose run -exec --rm django python manage.py makemigrations
  docker compose run -exec --rm django python manage.py migrate
}

case $COMMAND in
migrate)
  migrate
  ;;
*)
  echo 'No action specified!'
  ;;
esac
