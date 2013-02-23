#! /usr/bin/env python

"""Tests the Grocery service."""

import unittest
import logging
from pprint import pprint, pformat

from pyamf.remoting import ErrorFault

import client

def call(testcase, function, *args, **kwargs):
    """calls service function and asserts that response is not an error"""
    resp = function(*args, **kwargs)
    testcase.assert_(not isinstance(resp, ErrorFault), resp)
    return resp

class RetailStoreTest(unittest.TestCase):
    """Creates a retail store named 'foo'.  Modifies it and deletes it.
    """
    def runTest(self):
        try:
            service = client.connect()
            #print 'Connecting to %s' % service
            id = service.create('RetailStore', dict(name='foo'))
            #print 'id=%s (%s)' % (id, type(id))
            self.assert_(isinstance(id, (int, long)),
                         'id=%s (%s)' % (id, type(id)))
            error = service.create('RetailStore', dict(name='foo'))
            #print error
            self.assert_(isinstance(error, ErrorFault), error)
            fetched = service.fetch('RetailStore', [('name', '=', 'foo')], 1)
            if isinstance(fetched, ErrorFault): self.fail(fetched)
            fetched_id, fetched_store = fetched
            self.assertEqual(id, fetched_id, fetched_id)
            self.assertEqual('foo', fetched_store['name'])
            service.update('RetailStore', id, dict(name='bar'))
            self.assertEqual('bar', service.get('RetailStore', id)['name'])
        finally:
            service.delete('RetailStore', id)
            self._make_assertions(None, service.get('RetailStore', id))
        
    def _make_assertions(self, expected, actual):
        logging.debug('expect: %s' % expected)
        logging.debug('actual: %s' % actual)
        if expected:
            match = (tuple(expected.iteritems()) == tuple(actual.iteritems()))
        else: 
            match = actual is None
        logging.debug('match: %s' % match)
        self.assert_(match, 'expected: %s, actual: %s' % (expected, actual))
        logging.debug('--')

class HouseholdMemberTest(unittest.TestCase):

    def runTest(self):
        try:
            service = client.connect('test1@etapic.name')
            hid = service.create('Household', dict(name='my-household'))
            self.make_assertion(hid)
            hmid = service.create('HouseholdMember', dict(household=hid))
            self.make_assertion(hmid)
            hms = service.fetch('HouseholdMember')
            self.make_assertion(hms)
        finally:
            d_hm = service.delete('HouseholdMember', hmid)
            try:
                self.assert_(not isinstance(d_hm, ErrorFault), d_hm)
            finally:
                d_h = service.delete('Household', hid)
                self.assert_(not isinstance(d_h, ErrorFault), d_h)

    def make_assertion(self, value):
        self.assert_(value and not isinstance(value, ErrorFault), value)

class StartsWithTest(unittest.TestCase):
    """Tests fetch with a startswith operator in the where clause
    """
    def runTest(self):
        try:
            service = client.connect()
            sid = service.create('StoreSection', dict(name='cold cuts'))
            ids = []
            ids.append(call(self, service.create, 'ItemDescription', dict(store_section=sid,
                                                   description='bologna',
                                                   is_default=True)))
            ids.append(call(self, service.create, 'ItemDescription', dict(store_section=sid,
                                                   description='turkey',
                                                   is_default=True)))
            ids.append(call(self, service.create, 'ItemDescription', dict(store_section=sid,
                                                   description='Turkey Pastrami',
                                                   is_default=True)))
            ids.append(call(self, service.create, 'ItemDescription', dict(store_section=sid,
                                                   description='tuscan salami',
                                                   is_default=True)))
            ids.append(call(self, service.create, 'ItemDescription', dict(store_section=sid,
                                                   description='tuq',
                                                   is_default=True)))
            turkey_meats = service.fetch('ItemDescription',
                                         [('description', 'startswith', 'tur')])
            self.assert_(not isinstance(turkey_meats, ErrorFault), turkey_meats)
            self.assert_(len(turkey_meats) == 2, len(turkey_meats))
            descriptions = [dct['description'] for id, dct in turkey_meats]
            self.assert_('turkey' in descriptions, descriptions)
            self.assert_('Turkey Pastrami' in descriptions, descriptions)

        finally:
            for id in ids:
                call(self, service.delete, 'ItemDescription', id)
            call(self, service.delete, 'StoreSection', sid)

class IndirectFetchTest(unittest.TestCase):
    """Tests fetching entities indirectly.  For example ListItem doesn't have
    a reference property for store, but a logged in user can fetch the list
    items from the latest shopping list by providing only the store id.
    """
    def runTest(self):
        l1id = l2id = desc_id = hmid = sid = hid = milk_id = dairy_id = None
        try:
            # login
            service = client.connect('test1@etapic.name')
            # create household
            hid = call(self, service.create, 'Household', dict(name='my household'))
            # create household member
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
            # create store
            sid = call(self, service.create, 'RetailStore', dict(name='The Store'))
            # create list
            l1id = call(self, service.create, 'ShoppingList', dict(RetailStore=sid))
            # fetch list limit=1
            list1id, list1 = call(self, service.fetch, 'ShoppingList', 
                    [('RetailStore', '=', sid)], 1)
            items = call(self, service.fetch, 'ListItem', 
                    [('list', '=', list1id)])
            # assert that list is empty
            self.failIf(items, items)
            # create dairy section
            dairy_id = call(self, service.create, 'StoreSection', dict(name='Dairy'))
            # create milk item description
            desc_id = call(self, service.create, 'ItemDescription',
                    dict(description='milk', store_section=dairy_id))
            # create milk shopping item
            milk_id = call(self, service.create, 'ListItem',
                    dict(list=l1id, item_description=desc_id, quantity=1))
            # fetch list limit=1
            list2id, list2 = call(self, service.fetch, 'ShoppingList', 
                    [('RetailStore', '=', sid)], 1)
            items2 = call(self, service.fetch, 'ListItem', 
                    [('list', '=', list2id)])
            # assert that list contains milk
            self.assert_(len(items2) == 1, items2)
            actual_milk = items2[0][1].item_description
            self.assertEqual('milk', actual_milk.description, actual_milk)
            self.assertEqual('Dairy', actual_milk.store_section.name, actual_milk)
            # email the list
            call(self, service.mail_list, 
                 dict(recipient='brian.mabry.edwards@gmail.com', list_id=list2id))
            # create list
            l2id = call(self, service.create, 'ShoppingList', dict(RetailStore=sid))        
            # fetch list limit=1
            list3id, list3 = call(self, service.fetch, 'ShoppingList', 
                    [('RetailStore', '=', sid)], 1)
            items3 = call(self, service.fetch, 'ListItem', 
                     [('list', '=', list3id)])
            # assert that list is empty
            self.failIf(items3, items3)
        
        finally:
            # clean up
            if l1id: call(self, service.delete, 'ShoppingList', l1id)
            if l2id: call(self, service.delete, 'ShoppingList', l2id)
            if desc_id: call(self, service.delete, 'ItemDescription', desc_id)
        
            hslist = call(self, service.fetch, 'HouseholdStore', [])
            try:
                self.assertEqual(1, len(hslist), pformat(hslist))
            finally:
                for hs_id, info in hslist:
                    call(self, service.delete, 'HouseholdStore', hs_id)
        
                if hmid: call(self, service.delete, 'HouseholdMember', hmid)
                if hid: call(self, service.delete, 'Household', hid)
                if sid: call(self, service.delete, 'RetailStore', sid)
                if dairy_id: call(self, service.delete, 'StoreSection', dairy_id)
                if milk_id: call(self, service.delete, 'ListItem', milk_id)


class ListListTest(unittest.TestCase):
    """
    Tests listing all of a user's shopping lists.
    
    Load all of the user's lists. Show them in a list with the store name and 
    date.
    """
    def runTest(self):

        try:
            # login
            service = client.connect('test1@etapic.name')

            # create household
            hid = call(self, service.create, 'Household', dict(name='my household'))

            # create household member
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))

            # create store
            s0id = call(self, service.create, 'RetailStore', dict(name='Store 0'))
            s1id = call(self, service.create, 'RetailStore', dict(name='Store 1'))

            # create lists for both stores
            l0id = call(self, service.create, 'ShoppingList', dict(RetailStore=s0id))
            l1id = call(self, service.create, 'ShoppingList', dict(RetailStore=s1id))
        
            # fetch those lists
            lists = call(self, service.fetch, 'ShoppingList')
            self.assertEqual(2, len(lists), lists)

            def make_assertions(expected_id, expected_name):
                for id, shop_list in lists:
                    if id == expected_id:
                        self.assertEqual(shop_list.household_store.retail_store.name,
                                         expected_name,
                                         shop_list)
                        break
                else:
                    self.fail('Did not find id=%s in lists' % expected_id)
        
            make_assertions(l0id, 'Store 0')
            make_assertions(l1id, 'Store 1')

        finally:
            # clean up
            call(self, service.delete, 'ShoppingList', l1id)
            call(self, service.delete, 'ShoppingList', l0id)
            call(self, service.delete, 'RetailStore', s1id)
            call(self, service.delete, 'RetailStore', s0id)
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)


class FetchSectionsTest(unittest.TestCase):
    """Tests fetching all store sections."""
    def runTest(self):
        try:
            service = client.connect()
            a_id = call(self, service.create, 'StoreSection', dict(name='sect A'))
            b_id = call(self, service.create, 'StoreSection', dict(name='sect B'))
            c_id = call(self, service.create, 'StoreSection', dict(name='sect C'))
        
            # passing the empty list of filters is very important, otherwise the
            # filters argument might be changed by the other tests (?!?!?!?!?!?!)
            # and this call will return an empty list as the result
            sects = call(self, service.fetch, 'StoreSection', [])
            self.assert_(len(sects) == 3, len(sects))
            sects = dict(sects)
            self.assert_(sects[a_id]['name'] == 'sect A', sects[a_id]['name'])
            self.assert_(sects[b_id]['name'] == 'sect B', sects[b_id]['name'])
            self.assert_(sects[c_id]['name'] == 'sect C', sects[c_id]['name'])

        finally:
            call(self, service.delete, 'StoreSection', c_id)
            call(self, service.delete, 'StoreSection', b_id)
            call(self, service.delete, 'StoreSection', a_id)


class FetchHouseholdStoreTest(unittest.TestCase):
    """
    Test fetching a household store.
    """
    def runTest(self):

        try:
            # login
            service = client.connect('test1@etapic.name')

            # create household
            hid = call(self, service.create, 'Household', dict(name='my household'))

            # create household member
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))

            # create store
            s0id = call(self, service.create, 'RetailStore', dict(name='Store 0'))

            # create household store
            hsid = call(self, service.create, 'HouseholdStore', 
                    dict(household=hid, retail_store=s0id))

            # fetch household stores
            fetched = call(self, service.fetch, 'HouseholdStore', [])
            self.assert_(1 == len(fetched), fetched)
            self.assert_(fetched[0][1]['household']['name'] == 'my household')
            self.assert_(fetched[0][1]['retail_store']['name'] == 'Store 0')

        finally:
            # clean up
            call(self, service.delete, 'HouseholdStore', hsid)
            call(self, service.delete, 'RetailStore', s0id)
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)


class FetchListByHouseholdStore(unittest.TestCase):
    """
    Tests fetching a ShoppingList by HouseholdStore.  The other way is to use
    a RetailStore id in the fetch.
    """
    def runTest(self):

        try:
            # create stuff
            service = client.connect('test1@etapic.name')
            hid = call(self, service.create, 'Household', dict(name='my household'))
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
            s0id = call(self, service.create, 'RetailStore', dict(name='Store 0'))
            s1id = call(self, service.create, 'RetailStore', dict(name='Store 1'))
            hsid = call(self, service.create, 'HouseholdStore', 
                    dict(household=hid, retail_store=s0id))
            l0id = call(self, service.create, 'ShoppingList', dict(RetailStore=s0id))
            l1id = call(self, service.create, 'ShoppingList', dict(RetailStore=s1id))

            # fetch the list using HouseholdStore - should return l0, but not l1
            lists = call(self, service.fetch, 'ShoppingList', 
                    [('HouseholdStore', '=', hsid)])
            self.assertEqual(1, len(lists), pformat(lists))

            def make_assertions(expected_id, expected_name):
                for id, shop_list in lists:
                    if id == expected_id:
                        self.assertEqual(shop_list.household_store.retail_store.name,
                                         expected_name,
                                         shop_list)
                        break
                else:
                    self.fail('Did not find id=%s in lists' % expected_id)

            make_assertions(l0id, 'Store 0')

        finally:
            # clean up
            call(self, service.delete, 'ShoppingList', l1id)
            call(self, service.delete, 'ShoppingList', l0id)
            call(self, service.delete, 'HouseholdStore', hsid)
            call(self, service.delete, 'RetailStore', s1id)
            call(self, service.delete, 'RetailStore', s0id)
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)


class SecondHouseholdTest(unittest.TestCase):
    """
    Make sure that 2nd user does not fetch the first user's household-member.
    """
    
    def runTest(self):

        try:
            # login as test1 and create a household
            service = client.connect('test1@etapic.name')
            hid = call(self, service.create, 'Household', dict(name='test1 household'))
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
        
            # login as test2 and fetch household
            service2 = client.connect('test2@etapic.name')
            fetched = call(self, service2.fetch, 'HouseholdMember', [])
        
            # assert that the fetched list is empty
            self.assertEqual(0, len(fetched), pformat(fetched))

        finally:
            # clean up
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)
        

class ItemRecommendationTest(unittest.TestCase):
    """
    Tests fetching item recomendations
    """
    def runTest(self):

        try:
            # login and create stuff
            service = client.connect('test1@etapic.name')
            hid = call(self, service.create, 'Household', dict(name='my household'))
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
            sid = call(self, service.create, 'RetailStore', dict(name='The Store'))
            hsid = call(self, service.create, 'HouseholdStore', dict(retail_store=sid))
            dairy_id = call(self, service.create, 'StoreSection', dict(name='Dairy'))
            desc_id = call(self, service.create, 'ItemDescription',
                    dict(description='milk', store_section=dairy_id))

            # fetch recommendations and make assertions
            recommendations = call(self, service.fetch, 'ItemRecommendation',
                    [('StoreSection', '=', dairy_id)])
            self.assertEqual(1, len(recommendations), pformat(recommendations))
            for id, rec in recommendations:
                self.assertEqual('milk', rec.description)
                self.assertEqual('Dairy', rec.store_section.name)

        finally:
            # clean up
            call(self, service.delete, 'ItemDescription', desc_id)
            call(self, service.delete, 'StoreSection', dairy_id)
            call(self, service.delete, 'HouseholdStore', hsid)
            call(self, service.delete, 'RetailStore', sid)
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)


class FetchHouseholdTest(unittest.TestCase):
    """
    Tests creating a household and HouseholdMember and then fetching the 
    Household.
    """
    def runTest(self):

        try:
            # create stuff
            service = client.connect('test1@etapic.name')
            hid = call(self, service.create, 'Household', dict(name='my household'))
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
        
            # fetch and make assertions
            results = call(self, service.fetch, 'HouseholdMember', [])
            self.assertEqual(1, len(results))

        finally:
            # clean up
            call(self, service.delete, 'HouseholdMember', hmid)
            call(self, service.delete, 'Household', hid)


class CreateShoppingListTest(unittest.TestCase):
    """
    Tests creating a ShoppingList first by specfying a RetailStore, then by
    specifying a HouseholdStore.
    """
    
    def runTest(self):
        hid = hmid = rsid = None
        try:
            service = client.connect('test1@etapic.name')
            hid = call(self, service.create, 'Household', dict(name='foo household'))
            hmid = call(self, service.create, 'HouseholdMember', dict(household=hid))
            rsid = call(self, service.create, 'RetailStore', dict(name='Big Box'))
        
            # create ShoppingList by passing in RetailStore
            slid = hsid = None
            try:
                slid = call(self, service.create, "ShoppingList", 
                            dict(RetailStore=rsid))
                # creating a ShoppingList in this manner in turn creates a
                # HouseholdStore behind the scenes
                hsid, _ = call(self, service.fetch, 'HouseholdStore',
                            [("retail_store", "=", rsid)], 1)
                self.assert_(hsid is not None, str(hsid))
            finally:
                if slid: call(self, service.delete, "ShoppingList", slid)
                if hsid: call(self, service.delete, "HouseholdStore", hsid)
        
            # create ShoppingList by passing in HouseholdStore
            hsid2 = slid2 = None
            try:
                hsid2 = call(self, service.create, 'HouseholdStore',
                             dict(retail_store=rsid))
                slid2 = call(self, service.create, "ShoppingList", 
                             dict(HouseholdStore=hsid2))
            finally:
                if slid2: call(self, service.delete, "ShoppingList", slid2)
                if hsid2: call(self, service.delete, 'HouseholdStore', hsid2)
            
        finally:
            if rsid: call(self, service.delete, 'RetailStore', rsid)
            if hmid: call(self, service.delete, 'HouseholdMember', hmid)
            if hid: call(self, service.delete, 'Household', hid)


class LikeFilterTest(unittest.TestCase):
    def runTest(self):
        ids = []
        try:
            service = client.connect()
            for name in "barfooquux", "FoOquux", "bar":
                ids.append(call(self, service.create, 
                        "RetailStore", {"name": name}))
            pairs = call(self, service.fetch, 
                    "RetailStore", [("name", "like", "foo")])
            self.assertEqual(ids[:2], [id for id, _ in pairs])
        finally:
            for id in ids: call(self, service.delete, "RetailStore", id)


class CloneTest(unittest.TestCase):
    
    def runTest(self):
        
        ids = []
        service = client.connect()
        
        try:
            
            ids.append(
                call(self, service.create, "RetailStore", {"name": "st0"}))
                
            st0 = call(self, service.get, "RetailStore", ids[0])
            
            error = service.clone(st0["_key"], {"name": "st0"})
            self.assert_(isinstance(error, ErrorFault), error)
            
            ids.append(
                call(self, service.clone, st0["_key"], {"name": "st1"}))
        
        finally:
            
            for id in ids:
                call(self, service.delete, "RetailStore", id)

if __name__ == '__main__':
    unittest.main()
