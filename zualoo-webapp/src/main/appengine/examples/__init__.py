# Google App Engine for Flash projects with PyAMF. 
# Copyright (c) 2008 Aral Balkan (http://aralbalkan.com)
# Released under the Open Source MIT License
#
# Blog post: http://aralbalkan.com/1307 
# Google App Engine: http://code.google.com/appengine/
# PyAMF: http://pyamf.org

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import logging
from urlparse import urlparse
import os

from gaeswf import BaseSWFHandler


class InitialFlexExample(BaseSWFHandler):

	def get(self, path):
		
		# This is the root app URL that maps to this application in app.yaml.
		# If this application is accessed from root, set appUrl = '/'. 
		# In all other cases, set appUrl to the URL defined in your app.yaml 
		# file with a trailing forward slash but _without_ a forward slashe
		# at the end (e.g. /examples/swfaddress is correct).
		appUrl = "/"
		
		# Path to the example SWF
		swf = 'http://' + urlparse(self.request.url).netloc + '/static/swf/ShoppingList.swf';

		# Handle deep links
		self.handleDeepLinks(appUrl);

		template_values = {
			'type': 'Flex',
			'title': 'Shopping List',
			'description': '',
			'appUrl': appUrl,
			'swf': swf,
			'width': '1000',
			'height': '600'			
		}

		# Write out the HTML file to embed the SWF.
		path = os.path.join(os.path.dirname(__file__), '../templates/example_initial.html')
		self.response.out.write(template.render(path, template_values, debug=True))