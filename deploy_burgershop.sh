#!/bin/bash
set -e

git pull
pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python manage.py collectstatic --noinput
python manage.py migrate
systemctl restart burgershop
systemctl reload nginx

echo deploy was completed successfully
