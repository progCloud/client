#!/usr/bin/python
import authentication
import loop
from os.path import expanduser
import settings
import getuserinput

def main_func():
	fo = open(settings.secrets_file, "rw+")
	email = fo.readline().rstrip()
	password = fo.readline().rstrip()
	watch_dir = fo.readline().rstrip()
	fo.close()
	if(authentication.authenticate_user(email,password)=='1'):
		print 'User Authenticated! Watching Directory'
		loop.watch_directory(watch_dir)
	else:
		getuserinput.enter()
		print 'Failed To Authenticate User'

if __name__ == '__main__':
    main_func()
	
