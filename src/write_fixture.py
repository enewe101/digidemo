#!/usr/bin/python

'''
	This makes a database-agnostic dump of the app data, which is
 	automatically reloaded whenever migrate is called.
'''

import sys
import os, errno
import digidemo.settings as settings
import json
import subprocess
from digidemo.settings import DATA_FIXTURE

# helper function
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# make some absolute paths that are needed
manage_command = os.path.join(settings.BASE_DIR, 'manage.py')
fixtures_dir = os.path.join(settings.BASE_DIR, 'digidemo/fixtures')
fixture_fname = os.path.join(fixtures_dir, DATA_FIXTURE+'.json')

# be sure the fixtures dir exists and open the file for writing
mkdir_p(fixtures_dir)
fixture_file = open(fixture_fname, 'w')

# dump the app testing data related to the digidemo models
fixture_file.write(
	subprocess.check_output([
		manage_command,
		'dumpdata',
		'--format=json',
		'--indent=2',
		'digidemo',
		'auth.User'
	])
)

print 'wrote fixture to %s' % fixture_fname

