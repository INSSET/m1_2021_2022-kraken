#!/bin/bash

# check params
die() {
  echo >&2 "$@"
  exit 1
}
[ "$#" -ge 1 ] || die "Usage: setup.sh [dev|prod]"

MODE=$1

if [ "$MODE" = "dev" ]; then

  rm ../admin/.env
  cp admin.env.dev ../admin/.env
  echo "Dev admin setup"

  rm ../backend/config/docker-skell/symfony/.env.example
  cp symfony.backend.env.dev ../backend/config/docker-skell/symfony/.env.example
  echo "Dev symfony setup"

fi

if [ "$MODE" = "prod" ]; then

  rm ../admin/.env
  cp admin.env.prod ../admin/.env
  echo "Prod admin setup"

  rm ../backend/config/docker-skell/symfony/.env.example
  cp symfony.backend.env.prod ../backend/config/docker-skell/symfony/.env.example
  echo "Prod symfony setup"

fi