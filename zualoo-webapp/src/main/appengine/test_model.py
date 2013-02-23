import unittest
import model
from services import grocery

class GroceryStoreTest(unittest.TestCase):
    
    def testGroceryStore(self):
        gstore = model.GroceryStore(name='Test Grocery Store')
        id = gstore.put().id()
        self.assert_(id)
        svc = grocery.GroceryService(model)
        x = svc.retrieve('GroceryStore', id)
        self.assert_(False, x)
        