# INSTALLATION

## PART 1 -- INSTALL DEPENDENCIES
1. Install Apache httpd webserver.

2. Install mod\_wsgi, and configure apache webserver to use it.  Verify that
	you can serve a simple wsgi test application on localhost

3. Install MySQL

4. Install Django

5. Install South

Note: you should test all of those installations and convince yourself that,
at lesat separately, each is working.  Refer to the software's specific
documentation and user communities to get set up help!


## PART 2 -- INSTALL DIGIDEMO, AND WIRE THINGS UP
6. Download digidemo.

7. Configure Apache / mod\_wsgi to load the digidemo app.  Copy the following 
	configuration files in place, removing the '.template' part, and filling 
	the holes with your machine-specific details

		<proj-root>/src/digidemo/httpd.conf.template
		<proj-root>/src/digidemo/settings.py.template
		<proj-root>/src/digidemo/wsgi.py.template

	Test your configuration by going to localhost/test_web in a browser

	Troubleshoot your problems using the apache error log. Normally you can 
	find it at /var/log/apache2/error_log

8. Configure digidemo to work with your database.  Copy this file in place, 
	removing the '.template', and adding your database specifics:

		<proj-root>/src/digidemo/me.cnf.template

	In that file, you will need to indicate a user and password for digidemo
	to use when connecting to mysql.  The default user is digidemo.  Use
	whatever you want, but you will need to actually 

		- create a database called 'digidemo'
		- add the digidemo user to your mysql server, and give it write 
			privileges to the digidemo database

	test your database by directly logging into it in the terminal using
	the mysql client.  Log in as the user you created for digidemo to make
	sure that it works and that you have the needed permissions. 

	in <proj-root>/src, run the commands 
		
		$ python manage.py schemamigration digidemo --initial
		$ python manage.py migrate digidemo
	
	Test your database configuration by going to localhost/test_db.
	
	If you got errors during this process, you'll need to look for errors in
	your mysql installation, your my.cnf configuration, and you might also
	check your apache error log.
