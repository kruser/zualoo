######################################################################
#
# The GAE SWF Project (http://gaeswf.appspot.com)
#
# Photo upload/download handlers. These manage photo requests.
# (Note that the authToken scheme exists because Flash's FileReference
# feature for uploads/downloads has a bug where it doesn't send along
# session information. We need the authToken to authenticate users
# for uploads.)
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

import wsgiref.handlers
from google.appengine.ext import webapp

from examples.model import Photo
from examples.model import UserProfile

from google.appengine.api import users
from google.appengine.ext import db

import logging

import string

class PhotoUploadHandler(webapp.RequestHandler):
	
	def post(self):
		authToken = self.request.get('authToken')
		
		photo = Photo.all().filter("authToken = ", authToken).get()

		#if photo == None:
		#	photo = Photo()
		#	photo.user = user

		if photo:
			logging.info("Storing photo...")
			photo.ip = self.request.remote_addr
		
			image = self.request.get('upload')

			photo.fileBlob = db.Blob(image)	
			photo.put()
			
			# Until the user crops the photo, set their hasPhoto to false 
			# so that uncropped photos don't show up in the stream.
			userProfile = UserProfile.all().filter("user = ", photo.user).get()
			userProfile.hasPhoto = False
			userProfile.put()

			# Return something for complete event to fire in Flash. (Thank you, Abdul Qabiz).
			# http://www.abdulqabiz.com/blog/archives/flash_and_actionscript/workaround_file_1.php
			# This gets returned as the data in the uploadCompleteData event.
			self.response.out.write(True)
		else:
			logging.info("Error: No such photo.")
			# Unauthorized	
			self.error(401)

						
class PhotoDownloadHandler(webapp.RequestHandler):

	def get(self):
		user = users.get_current_user()
		
		if user:
			photo = Photo.all().filter("user = ", user).get()
			
			if photo:
				logging.info("Returning image!")
				# TODO: We really need to return the right content-type. Right now I'm returning JPEG for everything.
				self.response.headers['Content-Type'] = "image/jpeg"
				
				#logging.info(photo.fileBlob)
				
				self.response.out.write(photo.fileBlob)
			else:
				logging.info("No photo found for user, returning default.")
				self.redirect('/static/images/no_image.jpg')
		else:
			# Unauthorized
			self.error(401)