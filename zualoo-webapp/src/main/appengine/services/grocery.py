from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail
import logging
import sys
import traceback
import pprint
import re
import model

def log_stack_trace():
    logging.error(''.join(traceback.format_exception(*sys.exc_info())))


def fetchResults(Model, query, filters, limit=1000, offset=0):
    """
    fetch the results of the query applying any post-fetch filters to the
    results.  'like' filter can not be applied to the query so filter in the 
    application code instead.
    """
    
    likeFilters = []
    for property, operator, value in filters:
        if operator == "like":
            if hasattr(Model, property):
                likeFilters.append((property, re.compile(value, re.I)))
            else:
                raise Exception("%s has no property %s" % (
                        Model.__name__, property))
    
    if likeFilters:
                
        filteredEntities = []

        # full table scan, do as little as possible in this loop
        for entity in query:
            for property, pattern in likeFilters:
                if not pattern.search(getattr(entity, property)):
                    break
            else:
                filteredEntities.append(entity)
                if len(filteredEntities) == limit + offset:
                    break
        
        entities = filteredEntities[offset:]
        
    else: # no like filters
        entities = query.fetch(limit, offset)
    
    return entities


def deleteDuplicates(Model, query):
    """
    Delete all entities returned by the query except for the one with the
    lowest ID
    """
    ids = sorted([entity.key().id() for entity in query], reverse=True)
    assert len(ids) > 0
    if len(ids) > 1:
        duplicate_keys = [db.Key.from_path(Model.kind(), id) for id in ids[:-1]]
        for duplicate_key in duplicate_keys:
            duplicate = Model.get(duplicate_key)
            duplicate.delete()


def checkForDuplicates(Model, dct, entity):
    """
    If Model defines a natural key then make sure that only one entity exists
    with the natural key described by the dct parameter (a dictionary).
    """
    query = Model.natural_query()
    if query:
        query.bind(**dct)
        count = query.count()
        assert count > 0
        if count > 1:
            deleteDuplicates(Model, query)
            msg = '%s %s already exists.'
            args = (Model.__name__, entity.natural_key())
            raise Exception, msg % args


class GroceryService(object):

    def __init__(self, model_module):
        self.model_module = model_module

    def create(self, kind, dct):
        msg = "grocery service call: create('%s', %s)"
        logging.debug(msg % (kind, pprint.pformat(dct)))
        try:
            Model = getattr(self.model_module, kind)
            dct = self._cleanseDct(dct, Model)
            entity = Model(**dct)
            key = entity.put()
            checkForDuplicates(Model, dct, entity) # might raise an exception
            return key.id()
        except Exception, e:
            log_stack_trace()
            raise e
    
    
    def clone(self, encodedKey, dct):
        """
        Create a new entity by copying all of the properties from the existing
        entitiy identified by the encodedKey parameter except for those
        properties that are explicitly set in the dct parameter (a 
        dictionary).
        """
        
        msg = "grocery service call: clone(%s, %s)"
        logging.debug(msg % (encodedKey, dct))
        
        try:
        
            key = db.Key(encodedKey)
            Model = getattr(self.model_module, key.kind())
            entity = db.get(key)
            
            if not entity:
                
                raise Exception("%s with key %s does not exist" % (
                        Model, encodedKey))
            
            dct = self._cleanseDct(dct, Model)
            kw = {}
            
            for p in entity.properties():
                kw[p] = dct.get(p, getattr(entity, p))
            
            newEntity = Model(**kw)
            newKey = newEntity.put()
            checkForDuplicates(Model, kw, newEntity) # might raise exception
            return newKey.id()
        
        except Exception, e:
        
            log_stack_trace()
            raise e


    def get(self, kind, id):
        msg = "grocery service call: get('%s', %s)"
        logging.debug(msg % (kind, id))
        try:
            return self._get_by_id(kind, id)
        except Exception, e:
            log_stack_trace()
            raise e

    def fetch(self, kind, filters=[], limit=1000, offset=0):
        """
        For kinds that are associated with a household, this method
        returns all of that kind's entities associated with the current user's
        household.  For kinds not associated with a household, this method
        returns all entities of that kind.
        
        The filters parameter is a list of triples describing the where clause
        of the query. The form of each filter is (property, operator, value).
        The operator can be any of the gql operators.  The same property can
        be in the list more than once.  In addition to the gql operators,
        aggregate opertors are defined.  "startswith" and "like" are the 
        available aggregate operators.
        """

        msg = "grocery service call: fetch('%s', %s, %s, %s)"
        logging.debug(msg % (kind, filters, limit, offset))
        
        try:
            
            Model = getattr(self.model_module, kind)
            
            if Model.associated_with_user:
                user = users.get_current_user()
            
                if user:
                    filters.append(('user', '=', user))
            
                else:
                    msg = 'user must be logged in to fetch %s'
                    raise Exception(msg % Model.__name__)
            
            query = Model.build_query(filters)
            entities = fetchResults(Model, query, filters, limit, offset)
            result = [(entity.key().id(), entity) for entity in entities]
            
            if limit == 1:
                if result: result = result[0]
                else: result = None
            
            msg = 'grocery service call: fetch result=%s'
            logging.debug(msg % pprint.pformat(result))

            return result
        
        except Exception, e:
            
            log_stack_trace()
            raise e


    def update(self, kind, id, dct):
        msg = "grocery service call: update('%s', %s, %s)"
        logging.debug(msg % (kind, id, pprint.pformat(dct)))
        def function(entity, **kwargs):
            prop_keys = entity.properties().keys()
            for kwarg_key in kwargs.keys():
                if kwarg_key in prop_keys:
                    setattr(entity, kwarg_key, kwargs[kwarg_key])
                else:
                    msg = "'%s' model has no property '%s'"
                    raise Exception, msg % (Model.__name__, key)
            entity.put()
        self._update(function, kind, id, **self._str_key_dct(dct)) 
        
        
    def delete(self, kind, id):
        """
        Delete the entity of the specified kind identified by id from the data
        store.
        """
        
        msg = "grocery service call: delete('%s', %s)"
        logging.debug(msg % (kind, id))
        
        def function(entity, **kwargs):
            entity.delete()
        
        self._update(function, kind, id)
        
        
    def mail_list(self, dct):
        """
        Send an e-mail message to recipient containing the details of the
        shopping list identified by list_id.
        """
        
        msg = "grocery service call: mail_list(%s)"
        logging.debug(msg % dct)
        
        recipient = dct["recipient"]
        list_id = dct["list_id"]
        
        list_key = db.Key.from_path('ShoppingList', list_id)
        list = model.ShoppingList.get(list_key)
        items = model.ListItem.all().filter('list =', list_key).fetch(1000)
        logging.debug("list_key=%s, # of items=%s" % (list_key, len(items)))
        
        # sort the items by section
        itemsBySection = {}
        for item in items:            
            section = item.item_description.store_section.name
            if not itemsBySection.has_key(section):
                itemsBySection[section] = []
            itemsBySection[section].append(item)
        
        # fill out the body of the e-mail
        body = ''
        for section in sorted(itemsBySection):
            body += "== %s\n\n" % section
            
            for item in itemsBySection[section]:
                body += '  * %s - %s\n' % (item.quantity, 
                                     item.item_description.description)
            body += "\n\n"
            
        store = list.household_store.retail_store.name
            
        mail.send_mail(sender=recipient,
                      to=recipient,
                      subject="%s Grocery List" % store,
                      body=body)
        
    
    def _cleanseDct(self, dct, Model):
        dct = self._str_key_dct(dct)
        dct = self._ids_to_keys(Model.properties(), dct)
        dct = Model.build_init_kwargs(dct, users.get_current_user)
        return dct
    
        
    def _str_key_dct(self, unicode_key_dct):
        str_key_dct = {}
        for str_key in [key.encode('UTF-8') for key in unicode_key_dct.keys()]:
            str_key_dct[str_key] = unicode_key_dct[str_key]
        return str_key_dct
        
        
    def _ids_to_keys(self, properties, dct):
        """
        Translates datastore ids to keys.  IDs are unique within a kind.  Keys
        are globally unique.  properties is the list of properties of a kind.
        dct is the mapping passed in by the client.  The client uses IDs for 
        everything.  The IDs must be transalted to keys on the server side.
        IDs come in as the value for reference properties, or as the value for
        a kind by name that isn't directly referenced in the model.
        """
        def generator():
            for key in dct.keys():
                if properties.has_key(key):
                    if isinstance(properties[key], db.ReferenceProperty):
                        yield key, properties[key].reference_class.__name__
                elif hasattr(self.model_module, key):
                    yield key, key
        for key, kind in generator():
            dct[key] = db.Key.from_path(kind, dct[key])
        return dct
    
    
    def _get_by_id(self, kind, id):
        return getattr(self.model_module, kind).get_by_id(id)
    
    def _update(self, function, kind, id, **kwargs):
        try:
            Model = getattr(self.model_module, kind)
            entity = self._get_by_id(kind, id)
            if entity:
                kwargs = self._ids_to_keys(Model.properties(), kwargs)
                function(entity, **kwargs)
            else:
                msg = 'no %s exists with id=%s'
                raise Exception(msg % (Model.__name__, id))
        except Exception, e:
            log_stack_trace()
            raise e
