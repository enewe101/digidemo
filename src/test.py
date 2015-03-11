#!/usr/bin/python

'''
	Runs tests using django-nose test runner.  
	By default the database is used from one run to the next.  If you have
	recently migrated your database, you need to run with the flag

		--rebuild

'''

import sys
import os 
from digidemo.settings import BASE_DIR
from subprocess import Popen, PIPE


def run_tests(do_rebuild_db, *args):

	manage_command = os.path.join(BASE_DIR, 'manage.py')
	command = [manage_command, 'test', '--nologcapture'] + list(args)

	# Set the environment variable that controls whether the db is rebuilt
	my_env = os.environ.copy()
	if do_rebuild_db:
		my_env['REUSE_DB'] = '0'

	else:
		my_env['REUSE_DB'] = '1'

	returncode = Popen(command, env=my_env).wait()
	return returncode


if __name__ == '__main__':
	
	do_rebuild_db = False
	if len(sys.argv)>1  and sys.argv[1] == '--rebuild':
		do_rebuild_db = True
		args = sys.argv[2:]

	else:
		args = sys.argv[1:]

	run_tests(do_rebuild_db, *args)



