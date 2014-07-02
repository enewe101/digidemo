user=$1
pwd=$2

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

mysqldump$user_phrase$pwd_phrase --no-create-info --replace --complete-insert digidemo > test_data.sql
