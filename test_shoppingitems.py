#test_shoppingitems.py

import unittest
import os
import json
from app import create_app, DB
from app.models import ShoppingItems

class ShoppingitemsTestCase(unittest.TestCase):
    """ Class with shopping list tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppingitem = {
            'itemname':'python book',
            'quantity': 1,
            'price' : 2000
            }
        with self.app.app_context():
            DB.create_all()

    def test_shoppingitem_creation(self):
        """ Test API can create a shopping item. """
        res = self.client().post('/shoppinglists/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('python book', str(res.data))

    def test_get_shoppingitems(self):
        """ Test API can get all shopping items in a shopping list. """
        res = self.client().post('/shoppinglists/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/shoppingitems/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('python book', str(res.data))

    def test_edit_shoppingitem(self):
        """ Test API can edit a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('python book', str(res.data))
        res = self.client().put('/shoppinglists/shoppingitems/1', data={
            'itemname':'Shoes',
            'quantity': 2,
            'price' : 500
            })
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('python bok', str(res.data))
        self.assertIn('Shoes', str(res.data))

    def test_delete_shoppingitem(self):
        """ Test API can delete a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('python book', str(res.data))
        res = self.client().delete('/shoppinglists/shoppingitems/1')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('python book', str(res.data))


    def tearDown(self):
        """ A method that is called after each test. """
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

if __name__ == '__main__':
    unittest.main()
