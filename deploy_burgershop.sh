#!/bin/bash
set -e

source .env
git pull
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
git_revision=$(git rev-parse HEAD)
https api.rollbar.com:443/api/1/deploy X-Rollbar-Access-Token:$ROLLBAR_TOKEN environment=$ROLLBAR_ENVIRONMENT revision=$git_revision
echo deploy was completed successfully
