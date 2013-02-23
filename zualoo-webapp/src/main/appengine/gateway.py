# Google App Engine for Flash projects with PyAMF. 
# Copyright (c) 2008 Aral Balkan (http://aralbalkan.com)
# Released under the Open Source MIT License
#
# Blog post: http://aralbalkan.com/1307 
# Google App Engine: http://code.google.com/appengine/
# PyAMF: http://pyamf.org

# PyAMF Flash Remoting (RPC) gateway.

import wsgiref.handlers
from pyamf.remoting.gateway.wsgi import WSGIGateway

import logging

# You can also use a wildcard to import services here.
from services import user
from services import photo
from services import grocery

import model

# Service mappings
s = {
	'user': user,
	'photo': photo,
	'grocery': grocery.GroceryService(model)
}

def main():
  application = WSGIGateway(s)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()