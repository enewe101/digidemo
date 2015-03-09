#!/usr/bin/python

'''
	clears the database, then reloads it using the manage.py migrate command
'''

import sys
import os, errno
import digidemo.settings as settings
import json
import subprocess
from subprocess import Popen, PIPE


def reset(user, pwd):
	manage_command = os.path.join(settings.BASE_DIR, 'manage.py')

	# work out the user arguments
	user_tokens = []
	if user is not None:
		user_tokens = ['-u', user]

	# work out the password arguments
	pwd_tokens = []
	if pwd is not None:
		pwd_tokens = ['-p'+pwd]
		
	# build the mysql database drop / create commands
	mysql_preamble = ['mysql'] + user_tokens + pwd_tokens + ['-e']
	drop_command = mysql_preamble + ['drop database digidemo;']
	create_command = mysql_preamble + ['create database digidemo;']

	# run mysql commands
	returncode = Popen(drop_command, stderr=subprocess.STDOUT).wait()
	if returncode > 0:
		print 'aborted'
		return returncode
	
	returncode = Popen(create_command, stderr=subprocess.STDOUT).wait()
	if returncode > 0:
		print 'aborted'
		return returncode

	# migration 
	returncode = Popen(
		[manage_command, 'migrate'], stderr=subprocess.STDOUT).wait()
	if returncode > 0:
		print 'aborted'
		return returncode
	# data loading
	fixture_name = settings.DATA_FIXTURE
	Popen([manage_command, 'loaddata', fixture_name], 
		stderr=subprocess.STDOUT).wait()
	if returncode > 0:
		print 'aborted'
		return returncode


if __name__ == '__main__':
	user = None
	try:
		user = sys.argv[1]
	except IndexError:
		pass

	pwd = None
	try: 
		pwd = sys.argv[2]
	except IndexError:
		pass

	reset(user, pwd)



