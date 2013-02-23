#
# Base class for handlers that want to implement SWF-based applications
# that support regular and SWFAddress-style deep links.
#

from google.appengine.ext import webapp
from urlparse import urlparse

class BaseSWFHandler (webapp.RequestHandler):
	def handleDeepLinks(self, appUrl):
		# Handle calls to a SWF example with deep links.
		
		url = self.request.uri
		parsed_url = urlparse(url)
		
		# If the URL deep links but not in the SWFAddress format,
		# translate the deep link into SWFAddress format (anchor syntax).
		# We calculate the SWF deep link using the appUrl specified above.
		# (Keep in mind that the app's URL and its actual location 
		# on the file system do not have to be in any way related so we
		# can't use the file system location to automate this.) 
		#
		# TODO: Can we get the URL mapping from the YAML file somehow?
		
		# Translate regular URLs to SWFAddress URLs 
		# (So http://my.com/deep/link becomes http://my.com/#/deep/link)
		
		path = parsed_url.path

		if appUrl == '/' and path != '/':

			#
			# Deep link: special case for root. 
			#

			first_slash = url.find('/',7)
			url = (url[:first_slash] + "/#" + url[first_slash:])
			self.redirect(url, True)

		elif path != appUrl and path != appUrl + '/':

			#
			# Deep link: generic case for any url deeper than root.
			#
			
			# Get the SWF deep link by ignoring everything before the app URL.
			swf_deep_link_index = url.rfind(appUrl) + len(appUrl)
			swf_deep_link = url[swf_deep_link_index:]
		
			# Create the new (SWFAddress) URL and redirect the browser.
			url = (url[:swf_deep_link_index] + "/#" + swf_deep_link)
			self.redirect(url, True)		
