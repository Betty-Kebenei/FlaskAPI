#test_shoppinglists.py

import unittest
import json
from app import create_app, DB

class ShoppingListTestCase(unittest.TestCase):
    """ Class with shopping list tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        with self.app.app_context():
            DB.create_all()
    
    def tearDown(self):
        """ A method that is called after each test. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

    #### HELPER METHODS #### 
    def user_registration(
            self,
            firstname="Betty",
            lastname="Kebenei",
            username="Berry",
            email="berry@berry.com",
            password="A1234a"):
        """ User registration helper method."""
        data = {
            'firstname':firstname,
            'lastname':lastname,
            'username' :username,
            'email':email,
            'password':password
        }
        return self.client().post('/auth/register', data=data)

    def user_logsin(self, email="berry@berry.com", password="A1234a"):
        """User logging in helper method."""
        data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=data)

    def current_list(self, listname="Mashujaa day"):
        """Shopping list creation helper method."""
        data = {'listname':listname}
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data=data)
        return res

    #### END OF HELPER METHODS ####

    def test_shoppinglist_creation(self):
        """ Test API can create a shopping list. """
        res = self.current_list()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Mashujaa day', str(res.data))

    def test_existing_shoppinglist(self):
        """ Test API can check if a shopping list already exists. """
        res = self.current_list()
        self.assertEqual(res.status_code, 201)
        self.assertIn('Mashujaa day', str(res.data))
        res = self.current_list()
        self.assertEqual(res.status_code, 409)

    def test_show_shoppinglist(self):
        """ Test API can get all shopping lists. """
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.current_list()
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Mashujaa day', str(res.data))

    def test_edit_shoppinglist(self):
        """ Test API can edit a shopping list. """
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'Cake ingredient'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('Cake ingredient', str(res.data))
        res = self.client().put(
            '/home/shoppinglists/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'Snacks'})
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('Cake ingredient', str(res.data))

    def test_delete_shoppinglist(self):
        """ Test API can delete a shopping list. """
        self.user_registration()
        result = self.user_logsin()
        self.assertEqual(result.status_code, 200)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'Snacks'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('Snacks', str(res.data))
        res = self.client().delete(
            '/home/shoppinglists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('Snacks', str(res.data))
        
if __name__ == '__main__':     
    unittest.main()
