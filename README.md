## Installation

When you install the Digidemo webapp, you have two options for how it will
be served, and this choice impacts what dependencies you install and how much
configuration you need to do.  If you are installing Digidemo for development
purposes, on your local machine, then you can use the webserver that comes
with Django.  This makes installation a bit easier :)

If you are deploying Digidemo on a remote server, or if you just want to do 
full-stack testing, then you will need to install apache and mod\_wsgi to play 
the role of webserver.


### Part 1 -- install dependencies

1. Install git

		# apt-get install git

	see http://git-scm.com/book/en/Getting-Started-Installing-Git

*If you are deploying perform steps 1 and 2, otherwise skip ahead to step 3.*

2. Install Apache httpd webserver.

		# apt-get install git

	see http://http://httpd.apache.org/download.cgi

3. Install mod\_wsgi, and configure apache webserver to use it.  Verify that
	you can serve a simple wsgi test application on localhost

		# apt-get install libapache2-mod-wsgi

	see https://code.google.com/p/modwsgi/

4. Install the X Virtual frame buffer, Xvfb:

		apt-get install xvfb

*Start here if you are getting set up for development!*
5. Install MySQL

		apt-get install mysql-server

	see http://dev.mysql.com/downloads/installer/

	You'll need to do some config here.  Use the MySQL documentation to get 
	through it!  Once it's installed and configured, you can test to make sure
	by running:
		
		`$ mysql -u <username> -p<password>` 

	That should take you to the mysql command-line tool (You'll see `mysql>`).

6. Install python headers

		apt-get install python-dev
		

7. Install pip

		sudo apt-get install python-pip

	see http://pip.readthedocs.org/en/latest/installing.html

8. Install MySQLdb

		apt-get install libmysqlclient-dev
		pip install MySQL-python
		

8. Install Django
	(may require Pillow; `$ pip install Pillow`)
	Run this in the terminal:
		
		$ pip install Django==1.6.5

9. Install Selenium (package for python)

		$ pip install selenium

10. Install pydenticon

		pip install pydenticon

11. Install haystack (package for python)

		$ pip install django-haystack==2.0.0 
		$ pip install whoosh==2.4

Note: you should do a quick test to make sure your MySQL and (if deploying) 
Apache installations are set up correctly.  Refer to the software's specific 
documentation and user communities to get set up help!


### Part 2 -- install digidemo, and wire things up
12. Download digidemo.  Go to wherever you want to want the digidemo project
	folder to be placed, and run

		$ git clone https://github.com/enewe101/digidemo.git

7. Configure the digidemo webapp.  You need to make a couple configurations
	which lets Digidemo run from whatever directory you just installed it 
	to.  Find the settings file, and copy it in place, but remove the 
	`.template` extension.  You will find it here, relative to your 
	installation location.

		<proj-root:digidemo>/src/digidemo/settings.py.template

	There's one spot you need to edit in there.  Look for "#<>#", and put
	the absolute path to the location of the digidemo folder that was created
	when you cloned.


8. *If you are deploying, skip this step*
	Now see if digidemo was configured correctly.  Go to 

		`<proj-root:digidemo>/src/`

	and run the command 

		`python manage.py runserver`

	Then open a browser, and go to 

		`localhost:8000/test`

	You should see the test page.  If you got import errors (probably when you 
	tried to run `runserver`, then go into 

		`<proj-root:digidemo>/src/digidemo/wsgi.py`

	and you will see that there are two commented-out lines that should be
	uncommented in that case.

7. *If you are installing for dev purposes, skip this step*. 
	Configure Apache and mod\_wsgi to load the digidemo app.  
	
	a. Copy the following in place, removing the `.template` extension.

		<proj-root>/src/digidemo/wsgi.py.template
	
		You shouldn't need to make any changes to it, unless you find that
		you get import errors later when you try to test.  If that happens,
		have a look inside the file, there are a few lines to uncomment which
		might resolve the problem.

	b. Move the following file to the place where apache conf files go.

		<proj-root>/src/digidemo/httpd.conf.template

		Normally apache conf files go in `/etc/apache2/`, but it depends on
		your apache installation.  Be careful not to overwrite the `httpd.conf`
		file that is already there, unless that's what you want to do.

		A better idea is to copy the contents of the `httpd.conf.template`
		into the existing `httpd.conf` file, and then make machine-specific
		edits to the copied part.

		You will need to indicate absolute paths to various subfolders of 
		your digidemo installation, so that apache knows where to look when
		serving your website. 

		I didn't mark the lines to edit here, because you basically need
		to edit them all.  You just need to fill in the absolute file paths
		to various locations in the project, as well as the server name, and
		an administrator contact email (it's displayed in the default apache 
		500 error message).

	c. Test your configuration by going to <host>/test/ in a browser
		on your local machine.  Sub in the actual host name that is registered
		for your machine's public IP address for <host>.  

		Troubleshoot your problems using the apache error log. Normally you 
		can find it at /var/log/apache2/error.log


8. Configure digidemo to work with your database.  Copy this file in place, 
	removing the '.template' extension: 

		<proj-root>/src/digidemo/me.cnf.template

	That file tells the digidemo app how to connect to your MySQL database.
	Among other things, it specifies the username and password that the app
	uses when making that connection.  You'll can leave almost everything as-is
	but you'll need to provide a password: put it where you see "<pwd>".

	Now you need to go into MySQL do the following:
	a. create a database called 'digidemo'

		mysql> CREATE DATABASE digidemo character set utf8;

	b. create a user called 'digidemo' (give that user the same password you
		entered into `my.cnf`)

		mysql> CREATE USER 'digidemo'@'localhost' IDENTIFIED BY '<pwd>';

	c. give user `digidemo` full privileges for database `digidemo`.

		mysql> GRANT ALL ON digidemo.* TO 'digidemo'@'localhost';
		
	Try logging in as `digidemo` user in the terminal to make sure its working.

9.  Go to your home folder, and open either `.bashrc` or `.bash_profile`, 
	whichever one is there already. (Note that file names starting with a `.`
	are hidden by default.  Use `$ ls -a` to be able to see all files.)

	Put these line at the end of the file:

		`export PYTHONPATH=/path/to/digidemo/src:$PYTHONPATH`
		`export DJANGO_SETTINGS_MODULE=digidemo.settings`

	Note that you need to replace the `/path/to/digidemo/` part with the 
	path to the folder where you cloned digidemo.  Make sure you keep `/src`
	at the end.

	While still in your home folder, run

		$ source .bashrc

	Or use `.bash_profile`, depending on which file you edited.

	Now, make sure that the mysql server is running (run `$ mysqld`), and
	head back to `<proj-root:digidemo>/src`, and run:
		
		$ python manage.py syncdb

	You will be prompted to create a user at that time, say `no`. (some users
	get created for testing purposes automatically).

	If you get an error at this point that says 

		django.db.utils.OperationalError: (2002, "Can't connect to local MySQL 
		server through socket '/tmp/mysql.sock' (2)")

	Then either you forgot to startup the MySQL server (just run `$ mysqld`)
	or, it means that mysql didn't put its socket in the expected place.
	When the MySQL starts up, it makes a file-like object that other programs
	use to make connections.  You'll need to read the MySQL docs to figure
	out where it is putting that socket.  In my experience, if it isn't in 
	the default location specified in my.cnf.template, then check in 
	`/var/run/mysqld/mysqld.sock`.

	Once you figuer out where the socket is, go into 

		<proj-root:digidemo>/src/my.cnf

	and look for the line with #<>#, and put the absolute path to the socket.
	Now you can try running `$ python manage.py syncdb` again.

	Next, run:
		
		$ python manage.py collectstatic

	If prompted, say `yes`. You should see a bunch of files get copied over.

	Now, Go to `<proj-root:digidemo>/data` and run `$ ./load.sh`.


9. Quickly test to see if the app is running properly:
	If you've installed for development, go to `<proj-root:digidemo>/src`
	and run `$ python manage.py runserver` to start the development server,
	then go to:
	
		localhost:8000/mainPage

	if you are deploying, make sure that apache is running.  From any location
	run 

		sudo apachectl start

	or if it was running already, make sure its running with all your latest
	edits to confguration by restarting:

		sudo apachectl -k graceful

	Then, try to go to the mainPage using a browser on a local machine.  Go
	to `http://<host>/mainPage`, and of course replace <host> with the domain
	name that is registered for that server's public IP address.  Leave off
	the port number (but technically it should be :80, not :8000 which is 
	for the development server.)

	With some luck, you should see the main digidemo page!

10. You might want to run the search indexer to make search functionality 
	available.  Go to `<proj-root:digidemo>/src` and run:

		$ python manage.py rebuild_index
		$ python manage.py update_index

11. Now to make sure everything is completely installed correctly, run the
	testing suite.  

	*If you are running this on the deployment server*, you first need to
	start up the virtual framebuffer.

		sudo Xvfb :10 -ac

	Unfortunately it doesn't seem to be possible to run that in the background
	so, you'll need to ssh from another terminal to run the tests.

	Now, *whether you are installing for development or deployment*, 
	Go to `<proj-root:digidemo>/src`, and run 
	`$ python manage.py test`.  The tests take 1 - 2min to run at the moment.
	If you see any `broken pipe` errors, this is nothing to worry about, that
	is normal behavior of the browser, which drops connections when it sees
	that a certain page hasn't changed from the last request.  The number 
	of errors / failures will be printed at the very end.  If you see 'OK'
	it means there were no errors / failures.

12. Congratulations, you're done!

