######################################################################
#
# The GAE SWF Project (http://gaeswf.appspot.com)
#
# Model: Defines the persisted data types.
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

from google.appengine.ext import db
from google.appengine.api import users


class Photo(db.Model):
	user = db.UserProperty()
	fileBlob = db.BlobProperty()
	fileName = db.StringProperty(default=None)
	fileType = db.StringProperty(default=None)
	fileSize = db.IntegerProperty(default=0)
	modifiedAt = db.DateTimeProperty(auto_now=True)	
	authToken = db.StringProperty(default=None)
	ip = db.StringProperty(default=None)

class UserProfile(db.Model):
	user = db.UserProperty()
	name = db.StringProperty()
	url = db.LinkProperty()
	description = db.StringProperty()
	photo = db.ReferenceProperty(Photo)
	hasPhoto = db.BooleanProperty(default=False)
	createdAt = db.DateTimeProperty(auto_now_add=True)
	modifiedAt = db.DateTimeProperty(auto_now=True)
	
#class Stats(db.Model):
#	date = db.DateProperty()
#	newUsers = db.IntegerProperty() 
#	pageViews = db.IntegerProperty()
#	logins = db.IntegerProperty()
#	uniqueVisitors = db.IntegerProperty()
