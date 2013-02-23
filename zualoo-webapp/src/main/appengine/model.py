import logging
from google.appengine.ext import db

def _build_query(Model, filters, orders=[]):
    """produces a query. handles case-insensitive matches and the startswith
    operator
    """
    
    query = Model.all()
    
    for property, operator, value in filters:
        
        logging.debug("_build_query: filter %s %s %s" % (
                property, operator, value))
        
        if '%s_lower' % property in Model.properties().keys():
            property = '%s_lower' % property
            value = value.lower()
        
        # note: previous if block is not part of the following if/elif/else
        if operator == 'startswith':
            query.filter('%s >=' % property, value)
            query.filter('%s <' % property, 
                         value[:-1] + chr(ord(value[-1])+1))
        elif operator == "like":
            pass
        else:
            query.filter('%s %s' % (property, operator), value)
            
    for o in orders:
        query.order(o)
        
    return query
    
    
class RetailStore(db.Model):
    """A Retail Store"""

    name = db.StringProperty(required=True)
    associated_with_user = False

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def build_query(cls, filters):
        return _build_query(cls, filters)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE name = :name")

    def natural_key(self):
        return self.name

    def __repr__(self):
        format = "{name: %s}"
        args = (self.name)
        return format % args


class StoreSection(db.Model):
    """A section in the grocery store.  e.g. 'Produce'"""

    name = db.StringProperty(required=True)
    associated_with_user = False

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def build_query(cls, filters):
        return _build_query(cls, filters)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE name = :name")

    def natural_key(self):
        return self.name

    def __repr__(self):
        format = "{name: '%s'}"
        args = self.name
        return format % args


class ItemDescription(db.Model):
    """An item description.  The is_default property determines if this item
    shows up when a new ShopperStore is created"""

    store_section = db.ReferenceProperty(StoreSection, required=True)
    description = db.StringProperty(required=True)
    description_lower = db.StringProperty(required=True)
    is_default = db.BooleanProperty(required=True, default=False)
    associated_with_user = False

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def build_query(cls, filters):
        return _build_query(cls, filters)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE store_section = :store_section "
                       "AND description = :description")

    def __init__(self, parent=None, key_name=None, _app=None, **kwds):
        kwds['description_lower'] = kwds['description'].lower()
        db.Model.__init__(self, parent, key_name, _app, **kwds)

    def natural_key(self):
        return '%s::%s' % (self.store_section, self.description)

    def __repr__(self):
        format = "{store_section: '%s', description: '%s'}"
        args = (self.store_section, self.description)
        return format % args


class Household(db.Model):
    """A Household"""

    name = db.StringProperty(required=True)

    # This is defined later in this file
    # default_store = db.ReferenceProperty(HouseholdStore)

    associated_with_user = True

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def build_query(cls, filters):
        raise Exception, "fetch HouseholdMember instead of Household"
        
    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE name = :name ")

    def natural_key(self):
        return '%s' % (self.name)

    def __repr__(self):
        format = "{name: '%s'}"
        args = (self.name)
        return format % args
    

class HouseholdMember(db.Model):
    """Joins user to Household"""
    
    user = db.UserProperty(required=True)
    household = db.ReferenceProperty(Household, required=True)
    associated_with_user = True

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        dct['user'] = get_current_user()
        return dct

    @classmethod
    def build_query(cls, filters):
        return _build_query(cls, filters)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE user = :user")

    def natural_key(self):
        return '%s' % (self.user)

    def __repr__(self):
        format = "{user: '%s'}"
        args = (self.user)
        return format % args


def _household(user):
    """
    Gets the household of the user
    """
    return HouseholdMember.all().filter("user =", user).fetch(1)[0].household


def _build_household_query(Model, filters):
    """
    Creates a query translating the user filter found in filters to a
    household filter
    """
    _filters = []
    for property, operator, value in filters:
        if property == 'user':
            filter = 'household', '=', _household(value)
        else: filter = (property, operator, value)
        _filters.append(filter)
    return _build_query(Model, _filters)


class HouseholdAddress(db.Model):
    """an address associated with a household.  name could be 'home', 
    'work'"""
    
    name = db.StringProperty(required=True)
    household = db.ReferenceProperty(Household, required=True)
    line1 = db.StringProperty(required=True)
    line2 = db.StringProperty(required=True)
    city = db.StringProperty(required=True)
    state = db.StringProperty(required=True)
    zip = db.StringProperty(required=True)
    associated_with_user = True

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def build_query(cls, filters):
        return _build_household_query(cls, filters)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE name = :name "
                       "AND household = :household")

    def natural_key(self):
        return '%s::%s' % (self.name, self.household)

    def __repr__(self):
        format = "{name: '%s', household: '%s'}"
        args = (self.name, self.household)
        return format % args


class HouseholdStore(db.Model):
    """Joins a Household to a RetailStore"""

    household = db.ReferenceProperty(Household, required=True)
    retail_store = db.ReferenceProperty(RetailStore, required=True)
    associated_with_user = True

    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        dct['household'] = _household(get_current_user())
        return dct

    @classmethod
    def build_query(cls, filters):
        filters2 = []
        for property, operator, value in filters:
            if property == "retail_store":
                value2 = db.Key.from_path('RetailStore', value)
            else:
                value2 = value
            filters2.append((property, operator, value2))
        return _build_household_query(cls, filters2)

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE household = :household "
                       "AND retail_store = :retail_store")

    def natural_key(self):
        return '%s::%s' % (self.household, self.retail_store)

    def __repr__(self):
        format = "{household: '%s', retail_store: '%s'}"
        args = (self.household, self.retail_store)
        return format % args


Household.default_store = db.ReferenceProperty(HouseholdStore)


class ShoppingList(db.Model):
    
    household_store = db.ReferenceProperty(HouseholdStore, required=True)
    last_modified = db.DateTimeProperty(required=True, auto_now=True)
    associated_with_user = True
    
    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):

        if dct.has_key("HouseholdStore"):
            household_store = dct["HouseholdStore"]

        elif dct.has_key("RetailStore"):
            query = HouseholdStore.all()
            household = _household(get_current_user())
            query.filter('household =', household)        
            query.filter('retail_store =', dct['RetailStore'])
            if query.count() < 1:
                household_store = HouseholdStore(household=household,
                        retail_store=dct['RetailStore'])
                household_store.put()
            else:
                household_store = query.fetch(1)[0]
                
        else:
            raise Exception("no HouseholdStore or RetailStore specified")
            
        dct['household_store'] = household_store
        return dct
    
    @classmethod
    def _get_HouseholdStore(cls, filter_dct, hs_query):
        """
        Look at the filters and get the HouseholdStore to match on in the
        query.  This might include an indirect lookup by RetailStore, which in
        turn might include creating an appropriate HouseholdStore is none
        exists.
        """
        
        if filter_dct.has_key('HouseholdStore'):
            # fetch by HouseholdStore (class name)
            direct_key = 'HouseholdStore'
        elif filter_dct.has_key('household_store'):
            # fetch by household_store (property name)
            direct_key = 'household_store'
        else:
            # either an indirect lookup (RetailStore), or fetch all
            direct_key = None
            
            
        if direct_key:
            # direct lookup
            household_store = db.Key.from_path('HouseholdStore', 
                                               filter_dct[direct_key])
            
        elif filter_dct.has_key('RetailStore'):
            # fetch by RetailStore
            retail_store = db.Key.from_path('RetailStore', 
                                            filter_dct['RetailStore'])
            hs_query.filter('retail_store =', retail_store)
            if hs_query.count() == 0:
                household_store = HouseholdStore(household=household,
                                                 retail_store=retail_store)
                household_store.put()
            else:
                household_store = hs_query.fetch(1)[0]
        
        else:
            # fetch all
            household_store = None
        
        return household_store


    @classmethod
    def build_query(cls, filters):
        filter_dct = dict([(p, v) for p, _, v in filters])
        hs_query = HouseholdStore.all()
        household = _household(filter_dct['user'])
        hs_query.filter('household =', household)
        household_store = cls._get_HouseholdStore(filter_dct, hs_query)
                
        if household_store:
            # one specific store
            _filters = [('household_store', '=', household_store)]
            query = _build_query(cls, _filters, ['-last_modified'])
        else:
            # all stores for the current user
            hh_store_keys = [x.key() for x in hs_query.fetch(1000)]
            query = cls.gql("WHERE household_store IN :1", hh_store_keys)
        
        return query

    @classmethod
    def household_query(cls, household):
        hs_query = HouseholdStore.household_query(household)
        hss = hs_query.fetch(1000)
        query = cls.gql("WHERE household_store IN :1 "
                        "ORDER BY last_modified DESC")
        query.bind(hss)
        return query
    
    @classmethod
    def natural_query(cls):
        return None
                       
    def natural_key(self):
        return None
        
    def __repr__(self):
        format = "{household_store: '%s', last_modified: '%s'}"
        args = (self.household_store, self.last_modified)
        return format % args


class ListItem(db.Model):
    """A grocery item associated with a shopping list. Includes the quantity.
    """

    list = db.ReferenceProperty(ShoppingList, required=True)
    item_description = db.ReferenceProperty(ItemDescription, required=True)
    quantity = db.StringProperty(required=True)
    is_current = db.BooleanProperty(required=True, default=False)
    associated_with_user = False

    @classmethod
    def build_query(cls, filters):
        return _build_query(cls, [filters[0][:2] + \
                [db.Key.from_path('ShoppingList', filters[0][2])]])

    
    @classmethod
    def build_init_kwargs(cls, dct, get_current_user):
        return dct

    @classmethod
    def household_query(cls, household):
        """all the items of the current user's household"""
        hs_query = HouseholdStore.household_query(household)
        hss = hs_query.fetch(1000)
        query = cls.gql("WHERE household_store IN :1")
        query.bind(hss)
        return query

    @classmethod
    def natural_query(cls):
        return cls.gql("WHERE list = :list "
                       "AND item_description = :item_description")

    def __init__(self,
                parent=None,
                key_name=None,
                _app=None,
                _from_entity=False,
                **kwds):
        """
        Convert quantity to string.
        """
        kwds['quantity'] = str(kwds['quantity'])
        db.Model.__init__(self, parent, key_name, _app, _from_entity, **kwds)

    def natural_key(self):
        return '%s::%s' % (self.list, self.item_description)

    def __repr__(self):
        format = "{list: '%s', item_description: '%s'}"
        args = (self.list, self.item_description)
        return format % args


class ItemRecommendation(object):
    
    associated_with_user = False
    
    @classmethod
    def build_query(cls, filters):
        """
        Currently this simply returns a query for the ItemDescriptions in the
        StoreSection.
        """
        query = ItemDescription.all()
        filter_dct = dict([(p, v) for p, _, v in filters])
        query.filter("store_section =", 
                     db.Key.from_path('StoreSection', 
                                      filter_dct['StoreSection']))
        return query
