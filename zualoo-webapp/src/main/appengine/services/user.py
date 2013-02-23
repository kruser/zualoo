######################################################################
#
# The GAE SWF Project (http://gaeswf.appspot.com)
#
# Flash Remoting User methods: handle login, profile updates, etc.
# 
# Copyright (c) 2008 Aral Balkan. Released under the MIT license.
#
# Learn more about Google App Engine and other cool stuff at
# the Singularity Web Conference: Online on October 24-26, 2008
# http://singularity08.com
#
# Blog: http://aralbalkan.com
#
######################################################################

import logging

# Workaround for issue 128: Import the standard email library
# http://code.google.com/p/googleappengine/issues/detail?id=182
import email

from google.appengine.api import users
from google.appengine.ext import db

from google.appengine.api.mail import EmailMessage
from google.appengine.api.datastore_errors import BadValueError

from examples.model import UserProfile

from datetime import datetime
from datetime import timedelta

from pyamf import flex
from pyamf import amf3

def login(base_url, login_return_url):
		
	user = users.get_current_user()

	# The user value object (VO) contains login and logout URLs.
	# (With /gateway stripped out so that it returns to the SWF). 
	
	urls = getUrls(base_url, login_return_url)
	
	user_vo = {
		'login': urls['login'],
		'logout': urls['logout'],
		'auth': False
	}
	
	if user:
		# Add the user object to the user VO.
		user_vo['user'] = user
		user_vo['auth'] = True
		
		# Get the user's profile from the database
		profile = UserProfile.all().filter('user =', user).get()
		
		if profile == None:
			# User does not have a profile, create one!
			profile = UserProfile()
			profile.user = user
			profile.name = profile.url = None
			profile.save();
			
		user_vo['profile'] = {
			'name': profile.name,
			'url': profile.url,
			'description': profile.description,
			'key': str(profile.key())
		}

	return user_vo

# Given a base URL and a login return url, calculates the 
# login and logout urls.
def getUrls(base_url, login_return_url):
	# These urls require authentication. When logging out,
	# don't return the user to this url (return them to 
	# the root instead.)
	require_auth = {
		'/profile':True
	}
	
	login_url = users.create_login_url(base_url + login_return_url)
	
	# If the users current URL requires the user to be logged in, send them 
	# to the root. Otherwise, return them to the same public URL after logging out.
	try:
		require_auth[login_return_url]
	except KeyError:
		logout_url = users.create_logout_url(base_url + login_return_url) 
	else:
		logout_url = users.create_logout_url(base_url)

	return {'login': login_url, 'logout': logout_url}


def updateProfile(profileVO):
	user = users.get_current_user()
	
	if user:
		# Does the profile already exist?
		if profileVO.key == None:
			# No, create a new profile.
			profile = UserProfile()
			#logging.info("Creating a new profile!")
		else:
			# Yes, get the existing profile from the data store.
			profile = UserProfile.get(profileVO.key)
			#logging.debug("Updating existing profile...")
			
		# Update and save the profile.
		profile.user = user
		profile.name = profileVO.name
		profile.url = profileVO.url
		
		try:
			profile.description = profileVO.description
		except AttributeError:
			#logging.info("Profile description was empty, so we're skipping it.")
			pass

		profile.save()
			
		return {'name': profile.name, 'url': profile.url, 'description': profile.description, 'key': profileVO.key}
	
	return False
	
def validateURL(url):
	linkProperty = db.LinkProperty()

	try:
		linkProperty.validate(url)
	except BadValueError:
		return False
		
	return True 
	
	
def getRecentUsersWithPhotos():
	
	# Profiles with photos created in the last 12 hours.
	# last12Hours = datetime.utcnow()-timedelta(hours=12)
	# .filter('modifiedAt > ', last12Hours)
	userProfileQuery = UserProfile.all().filter('hasPhoto = ', True).order('-modifiedAt')
	
	# Get the last 10.
	results = userProfileQuery.fetch(10)
	
	# Make an array of the results (PyAMF is currently choking on result sets from the
	# DataStore)
	resultsArray = [];	
	for result in results:
		resultsArray.append({'name': result.name, 'url': result.url, 'description': result.description, 'photo': amf3.ByteArray(result.photo.fileBlob)})

	# An ArrayCollection is even better :) 
	resultsArrayCollection = flex.ArrayCollection(resultsArray)

	return resultsArrayCollection
	
	
	