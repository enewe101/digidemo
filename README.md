## Installation

This covers installation of the digidemo webapp for development purposes on a debian-based system, like Ubuntu.  For other cases, you'll need all the same
dependencies, but you won't be able to install them using apt-get.

### Part 0 -- get dependencies

1. Install a bunch of stuff using apt-get.  You can copy this single command to
	get all things, or you can apt-get install each package separately, or
	leave out the ones you know you already have.

		$ sudo apt-get install git mysql-server python-dev python-pip libmysqlclient-dev

2. Install a bunch of stuff using pip.  You can install all these separately, but if you already have a package, pip will just make sure it's up-to-date:

		$ sudo pip install MySQL-python Pillow Django==1.6.5 selenium pydenticon django-haystack==2.0.0 whoosh==2.4

3. Get the code for this project.  Let's say you keep your projects in the
	folder ~/my_projects/.  Go there and do:
		
		$ git clone https://github.com/enewe101/digidemo.git

### Part 1 -- wiring and config
4. Set up a database and user that the  digidemo webapp will use
		
	Head into mysql:

		$ mysql -u root

			OR

		$ mysql -u <username> -p

	If that didn't work, you probably need to start mysql server, and then 
	try again:

		$ mysqld

	Make a user and table for the digidemo web app.  When at the mysql prompt:

		mysql> CREATE DATABASE digidemo character set utf8;
		mysql> CREATE USER 'digidemo'@'localhost' IDENTIFIED BY 'devpass';
		mysql> GRANT ALL ON digidemo.* TO 'digidemo'@'localhost';
		mysql> GRANT ALL ON test_digidemo.* TO 'digidemo'@'localhost';
		
	Logout of mysql and try logging back in as `digidemo` user in the terminal 
`	to make sure its working.


5. Copy some configuration files in place.  Go to `~/my_projects/digidemo/src`
	and do:

		$ cp settings.py.template settings.py
		$ cp wsgi.py.template wsgi.py

	Go into settings and find spots where #<># occurs.  Make the changes
	to reflect the location where you put the digidemo code.

### Part 2 --- fire up and test the app
6. Get the digidemo app ready, then fire it up. 
	Inside `~/my_projects/digidemo/src` do:

		$ python manage.py syncdb
			(say `no` to creating a superuser)
		$ python manage.py collectstatic
			(say `yes` to copying files)
		$ ../data/load.sh
		$ python manage.py runserver`

	Then open a browser, and go to 

		`localhost:8000/`

	You should see the home page.  

7. Quickly run the tests to see if everything is all good.  In 
	`~/my_projects/digidemo/src`, do:

		$ python manage.py test

8. Congratulations, you're done!


### Other stuff
updating haystack index:

		$ python manage.py rebuild_index
		$ python manage.py update_index


### Notes about production server
There are some additional steps when installing the production server.
Here are a few of them:

1. Install mod\_wsgi, and configure apache webserver to use it.  Verify that
	you can serve a simple wsgi test application on localhost

		# apt-get install libapache2-mod-wsgi

	see https://code.google.com/p/modwsgi/

2. Install the X Virtual frame buffer, Xvfb:

		apt-get install xvfb

3. *If you are installing for dev purposes, skip this step*. 
	Configure Apache and mod\_wsgi to load the digidemo app.  
	Make the apache config.  You can base it off this file:

		~/my_projects/digidemo/src/digidemo/httpd.conf.template

4. To run tests on a headless server, start the virtual frame buffer:

		$ sudo Xvfb :10 -ac
		$ python manage.py test

	Unfortunately it doesn't seem to be possible to run that in the background
	so, you'll need to ssh from another terminal to run the tests.

