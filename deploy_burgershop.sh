#!/bin/bash
set -e

source .env
git pull
/opt/burgershop/env/bin/pip3 install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
/opt/burgershop/env/bin/python3 manage.py collectstatic --noinput
/opt/burgershop/env/bin/python3 manage.py migrate --noinput
systemctl restart burgershop
systemctl reload nginx

git_revision=$(git rev-parse HEAD)
https api.rollbar.com:443/api/1/deploy X-Rollbar-Access-Token:$ROLLBAR_TOKEN environment=$ROLLBAR_ENVIRONMENT revision=$git_revision
echo deploy was completed successfully
