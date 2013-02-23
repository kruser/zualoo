from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from pyamf.remoting.gateway.google import WebAppGateway
import logging
import model
from services import user
from services import grocery
import wsgiref.handlers
from os import path
from examples import InitialFlexExample

class MainRequestHandler(webapp.RequestHandler):
    
    def get(self, *args):
        path=self._path('main.html')
        dct={}
        self.response.out.write(template.render(path, dct, debug=True))
        
    def _path(self, file):
        return path.join(path.dirname(__file__), 'templates', file)


def main():
    srvcs = {'user': user,
             'grocery': grocery.GroceryService(model)}
    url_mapping=[('/amf/', WebAppGateway(srvcs)),
                 ('(/.*)', InitialFlexExample)]
    application=webapp.WSGIApplication(url_mapping, debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__=='__main__':
    main()
