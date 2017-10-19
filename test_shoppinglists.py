#test_shoppinglists.py

import unittest
from app import create_app, DB
from app.models import ShoppingList
from app.home import views

class ShoppingListTestCase(unittest.TestCase):
    """ Class with shopping list tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppinglist = {'listname':'Mashujaa day'}
        with self.app.app_context():
            DB.create_all()
    
    def tearDown(self):
        """ A method that is called after each test. """
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

    def test_shoppinglist_creation(self):
        """ Test API can create a shopping list. """
        res = self.client().post('/home/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Mashujaa day', str(res.data))

    def test_existing_shoppinglist(self):
        """ Test API can check if a shopping list already exists. """
        res = self.client().post('home/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Mashujaa day', str(res.data))
        res = self.client().post('home/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 404)


    def test_show_shoppinglist(self):
        """ Test API can get all shopping lists. """
        res = self.client().post('/home/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/home/shoppinglists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Mashujaa day', str(res.data))

    def test_edit_shoppinglist(self):
        """ Test API can edit a shopping list. """
        res = self.client().post('/home/shoppinglists/', data={'listname':'Cake ingredient'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('Cake ingredient', str(res.data))
        res = self.client().put('/home/shoppinglists/1', data={'listname':'Snacks'})
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('Cake ingredient', str(res.data))

    def test_delete_shoppinglist(self):
        """ Test API can delete a shopping list. """
        res = self.client().post('/home/shoppinglists/', data={'listname':'Snacks'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('Snacks', str(res.data))
        res = self.client().delete('/home/shoppinglists/1')
        self.assertEqual(res.status_code, 200)
        res = self.client().delete('/home/shoppinglists/1')
        self.assertNotEqual(res.status_code, 200)
        self.assertNotIn('Snacks', str(res.data))

if __name__ == '__main__':
    unittest.main()
