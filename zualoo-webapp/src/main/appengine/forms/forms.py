"""
Serves as living documentation of the model. Uses djangoforms to provide 
evergreen CRUD access to the model with HTML forms.
"""

import wsgiref.handlers
import logging
import inspect
from os import path
from urllib import urlencode

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import users

# Note that you must import google.appengine.webapp.template before importing
# any Django modules. Pydev CTRL-O import organization breaks this.
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

import model

def template_path(name):
    return path.join(path.dirname(__file__), '%s.html' % name)

class ModelMetadata(object):

    def __init__(self, Model):
        self.props=sorted([(v.creation_counter, k, v.verbose_name) 
                           for k, v in Model.properties().items()])

    def attribute_names(self):
        """attribute names from Model in order of declaraion"""
        return [k for _, k, _ in self.props]

    def headers(self):
        """header labels for Model in order of declaration"""
        headers=[]
        for _, k, verbose_name in self.props:
            if verbose_name: label=verbose_name
            else: label=k.replace('_', ' ').title()
            headers.append(label)        
        return headers

class BaseHandler(object):

    def __init__(self, path_info, user, params):
        self.path_info = path_info
        self.user = user
        self.params = params
        self.Model = getattr(model, path_info[0])
        self.meta = ModelMetadata(self.Model)
    
    def feedback(self, entity, format):
        first_attribute = getattr(entity, self.meta.attribute_names()[0])
        return {'feedback': format % (self.Model.__name__, first_attribute)}

class ListHandler(BaseHandler):
    """handles the list functionality"""

    def get(self):
        path = template_path('list')
        dct = {}
        dct['entities'] = self.Model.all().fetch(1000)
        for entity in dct['entities']:
            entity.attributes = [getattr(entity, name) 
                                     for name in self.meta.attribute_names()]
        dct['headers'] = self.meta.headers()
        dct['feedback'] = self.params.get('feedback')
        dct['model_name'] = self.Model.__name__
        return path, dct
        
    def post(self):
        if self.params.get('edit'): uri = self.edit()
        elif self.params.get('delete'): uri = self.delete()
        else: raise Exception('post failed')
        return uri

    def edit(self):
        return '../editor/%s?%s' % (self.Model.__name__, urlencode(self.params))

    def delete(self):
        entity = self.Model.get_by_id(int(self.params.get('id')))
        entity.delete()
        dct = self.feedback(entity, '%s "%s" was deleted.')
        return '../list/%s?%s' % (self.Model.__name__, urlencode(dct))

        
class EditorHandler(BaseHandler):
    """handles the editor functionality"""
    def __init__(self, path_info, user, params):
        BaseHandler.__init__(self, path_info, user, params)
        class Form(djangoforms.ModelForm): 
            class Meta: model = self.Model
        self.Form = Form

    def get(self):
        path = template_path('editor')
        if self.params.get('invalid'): data = self.params
        else: data = None
        dct = {}
        dct['model_form'] = self.Form(data=data, instance=self.fetch())
        dct['id'] = self.params.get('id')
        dct['model_name'] = self.Model.__name__
        return path, dct
    
    def post(self):
        if self.params.get('save'): uri = self.save()
        elif self.params.get('cancel'): uri = self.cancel()
        else: raise Exception('post failed')
        return uri

    def save(self):
        input = self.Form(data=self.params, instance=self.fetch())
        if input.is_valid():
            entity = input.save(commit=False)
            entity.put()
            dct = self.feedback(entity, '%s "%s" was saved.')
            uri = '../list/%s?%s' % (self.Model.__name__, urlencode(dct))
        else:
            query = {'invalid': 1}
            query.update(self.params)
            uri='../editor/%s?%s' % (self.Model.__name__, urlencode(query))
        return uri
    
    def cancel(self):
        return '../list/%s' % self.Model.__name__
    
    def fetch(self):
        id = self.params.get('id')
        if id: entity = self.Model.get_by_id(int(id))
        else: entity = None
        return entity

class IndexHandler(object):
    """lists all the model classes that are defined"""
    def __init__(self, *args):
        pass
    
    def get(self):
        path = template_path('index')
        dct = {'models': []}
        for name in dir(model):
            if name != 'HouseholdRelated':
                attr = getattr(model, name)
                if inspect.isclass(attr):
                    dct['models'].append(name)
        return path, dct
        
    def post(self):
        raise Exception('post not supported by IndexHandler')

class FormsRequestHandler(webapp.RequestHandler):
    
    Handlers = {'list': ListHandler,
                'editor': EditorHandler}
    
    def get(self, path_info=''):
        path, dct = self._handle(path_info, 'get')
        self.response.out.write(template.render(path, dct, debug=True))
        
    def post(self, path_info=''):
        uri = self._handle(path_info, 'post')
        self.redirect(uri)
        
    def _handle(self, path_info, method):
        user = users.get_current_user()
        return_uri = '/forms/' + path_info
        if not user: self.redirect(users.create_login_url(return_uri))
        parts = path_info.split('/')
        Handler = self.Handlers.setdefault(parts[0], IndexHandler)
        handler = Handler(parts[1:], user, self.request.params)
        return getattr(handler, method)()

def main():
    url_mapping=[(r'/forms/(.*)', FormsRequestHandler)]
    application=webapp.WSGIApplication(url_mapping, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__=='__main__':
    main()
