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

from google.appengine.api import users
from google.appengine.ext import db

from examples.model import Photo
from examples.model import UserProfile

from datetime import datetime

import md5

def getAuthToken(fileName, fileSize, fileType):
	""" 
	Return an auth token to the client. Client will send this 
	auth token back with its FileReference file upload request. 
	(This workaround is necessary because FileReference doesn't send
	session info.)
	"""
	
	user = users.get_current_user()

	if user:
		
		# Does a photo entry exist for this user? 
		photo = Photo.all().filter('user =', user).get()
				
		if photo == None:
			# First time user is uploading the photo, create it
			logging.debug("First time photo upload for user. Creating photo object.")
			photo = Photo()
			photo.user = user
			photo.put()

		logging.info("fileName = " + fileName)
		logging.info("fileSize = " + str(fileSize))
		logging.info("fileType = " + fileType)

		# Store the name, size, and type of the file being uploaded.
		# TODO: Filter here for file types?
		photo.fileName = fileName
		photo.fileSize = fileSize
		photo.fileType = fileType
		
		
		# Make an auth token hash that's valid only for this photo.
		photo.authToken = md5.new(str(photo.key()) + fileName + str(fileSize) + fileType + datetime.utcnow().strftime("%Y%m%dT%H%M%S")).hexdigest()
		photo.put()

		logging.debug('New auth token: ' + photo.authToken)
		
		return {'authToken': photo.authToken}
		
	else:

		# Unauthorized.
		logging.info('Not returning auth token to unauthorized user.')
		self.error(403)
	
		
def uploadByteArray(byteArray):
	""" 
	Allows the upload of a PNG encoded as a ByteArray from Flash for 
	authenticated users. (This is used to upload cropped images from Flash.)
	"""
	user = users.get_current_user()
	
	# Does a photo entry exist for this user? 
	photo = Photo.all().filter('user =', user).get()
			
	if photo == None:
		# Something's wrong. 
		self.error(500)
		
	photo.fileBlob = db.Blob(str(byteArray))
	photo.fileName = "Cropped bytearray"
	photo.fileSize = len(byteArray)
	photo.fileType = "PNG"
	photo.authToken = ""
	photo.put()
	
	userProfile = UserProfile.all().filter('user = ', user).get()
	
	userProfile.hasPhoto = True
	userProfile.photo = photo
	userProfile.put()
	
