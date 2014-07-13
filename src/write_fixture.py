#!/usr/bin/python

import sys
import os, errno
import digidemo.settings as settings
import json
import subprocess

# helper function
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise



#	DJANGO FIXTURE DUMPING
#
# 		This makes a database-agnostic dump of the app data, which is
# 		automatically reloaded whenever syncdb is called.


# make some absolute paths that are needed
manage_command = os.path.join(settings.BASE_DIR, 'manage.py')
save_command = os.path.join(settings.PROJECT_DIR, 'data/save.sh')
fixtures_dir = os.path.join(settings.PROJECT_DIR, 'data/fixtures')
fixture_fname = os.path.join(
	settings.PROJECT_DIR, 'data/fixtures/initial_data.json')


# dump the app testing data related to the digidemo models
digidemo_dump = subprocess.check_output([
	manage_command,
	'dumpdata',
	'--format=json',
	'--indent=4',
	'digidemo'
])


# dump the app testing data related to the auth.user model (test users)
auth_user_dump = subprocess.check_output([
	manage_command,
	'dumpdata',
	'--format=json',
	'--indent=4',
	'auth.User'
])


# merge the two dumps into one fixture
fixture = json.loads(auth_user_dump) + json.loads(digidemo_dump) 

# be sure the fixtures dir exists 
mkdir_p(fixtures_dir)

# write the fixture to initial_data.json
# this gets read when ./manage.py syncdb is executed
with open(fixture_fname, 'w') as fixture_file:
	fixture_file.write(json.dumps(fixture, indent=4))

print 'wrote fixture to %s' % fixture_fname


#	RAW SQL DUMPING
#
# 		now we make sql dumps 
# 		These contain basically the same info as the fixture, but as raw sql, 
#		so it could be loaded without going through django.  
#


# First build the save command.  The user can provide a username and password
# for database authentication, pass these through to another script that
# handles database dumping
save_call = [save_command]
if len(sys.argv) > 1:
	save_call.append(sys.argv[1])

if len(sys.argv) > 2:
	save_call.append(sys.argv[2])

# call the script that handles database dumping
subprocess.call(save_call)



