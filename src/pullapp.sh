#!/bin/bash

# pull latest version of code from repo
git pull

# copy any now static files to the correct location
./manage.py collectstatic --noinput

# set permissions to copied files
chown -R www-data:www-data ../static

# compile translation message files
cd digidemo
django-admin.py compilemessages
cd ..

# restart the server
apachectl -k graceful

