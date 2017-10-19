#test_shoppingitems.py

import unittest
import os
import json
from app import create_app, DB
from app.models import ShoppingList, ShoppingItems

class ShoppingitemsTestCase(unittest.TestCase):
    """ Class with shopping list tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppinglist = {'listname':'Visiting mum'}
        self.shoppingitem = {
            'itemname':'Wheat Flour',
            'quantity': 12,
            'price' : 1200
            }
        with self.app.app_context():
            DB.create_all()

    def test_shoppingitem_creation(self):
        """ Test API can create a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wheat Flour', str(res.data))

    def test_creation_fails(self):
        """ Test API can must create a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('Wheat Flour', str(res.data))

    def test_duplicate_creation(self):
        """ Test API cannot create items with same name in one a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wheat Flour', str(res.data))
        res = self.client().post('/shoppinglists/1/shoppingitems/', data={
            'itemname':'Wheat Flour',
            'quantity': 12,
            'price' : 1200
        })
        self.assertEqual(res.status_code, 404)

    def test_multiple_creations(self):
        """ Test API can create many items in one a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wheat Flour', str(res.data))
        res = self.client().post('/shoppinglists/1/shoppingitems/', data={
            'itemname':'Maize Flour',
            'quantity': 12,
            'price' : 1000
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('Maize Flour', str(res.data))

    def test_get_shoppingitems(self):
        """ Test API can get all shopping items in a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/1/shoppingitems/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Wheat Flour', str(res.data))

    def test_edit_shoppingitem(self):
        """ Test API can edit a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wheat Flour', str(res.data))
        res = self.client().put('/shoppinglists/1/shoppingitems/1', data={
            'itemname':'Rice',
            'quantity': 10,
            'price' : 1000
            })
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('WheatFlour', str(res.data))

    def test_delete_shoppingitem(self):
        """ Test API can delete a shopping item in a shopping list. """
        res = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/shoppinglists/1/shoppingitems/', data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Wheat Flour', str(res.data))
        res = self.client().delete('/shoppinglists/1/shoppingitems/1')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('Wheat Flour', str(res.data))


    def tearDown(self):
        """ A method that is called after each test. """
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

if __name__ == '__main__':
    unittest.main()
