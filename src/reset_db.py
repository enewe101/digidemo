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


manage_command = os.path.join(settings.BASE_DIR, 'manage.py')

Popen(['mysql', '-e', 'drop database digidemo;'], 
		stderr=subprocess.STDOUT).wait()

Popen(['mysql', '-e', 'create database digidemo;'], 
		stderr=subprocess.STDOUT).wait()

Popen([manage_command, 'migrate'], 
		stderr=subprocess.STDOUT).wait()

#output = os.popen("mysql -e 'drop database digidemo;'")
#output = os.popen("mysql -e 'create database digidemo;'")
#output = os.popen('%s migrate' % manage_command)

