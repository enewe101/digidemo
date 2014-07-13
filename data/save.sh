#!/bin/bash

user=$1
pwd=$2

# If the command was called with user and password arguments, then prepare
# them to be passed through to the mysql command
if [ "$user" == "" ]; then
	user_phrase=""
else
	user_phrase=" -u $user"
fi

if [ "$pwd" == "" ]; then
	pwd_phrase=""
else
	pwd_phrase=" -p$pwd"
fi

# get the data directory, where the sql dumps will be written
data_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# dump sql that completely refreshes the database schema and loads data
mysqldump$user_phrase$pwd_phrase --replace --complete-insert --add-drop-database --databases digidemo > $data_dir/load.sql

echo "wrote full database refresh dump to $data_dir/load.sql"

# dump sql that only loads data
mysqldump$user_phrase$pwd_phrase --no-create-info --replace --complete-insert --ignore=digidemo.south_migrationhistory digidemo > $data_dir/patch.sql

echo "wrote data insertion dump (no schemo info) to $data_dir/patch.sql"
