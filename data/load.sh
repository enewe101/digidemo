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

mysql$user_phrase$pwd_phrase digidemo < load.sql
mkdir -p ../media/
cp -r media/* ../media/
