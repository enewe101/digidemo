#!/bin/bash

# abort if any line fails
set -e

# backup database
./manage.py dumpdata --format=json --indent=2 digidemo auth.User > digidemo/fixtures/backup.json

# pull latest version of code from repo
git pull

# migrate the database
./manage.py migrate digidemo

# copy any new static files to the correct location
./manage.py collectstatic --noinput

# set permissions to copied files
chown -R www-data:www-data ../static

# compile translation message files
cd digidemo
django-admin.py compilemessages
cd ..

# restart the server
apachectl -k graceful

