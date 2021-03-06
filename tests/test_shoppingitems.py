#test_shoppingitems.py

import unittest
import json
from app import create_app, DB

class ShoppingitemsTestCase(unittest.TestCase):
    """ Class with shopping items tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shoppingitem = {
            'itemname':'wheat flour',
            'quantity': 12,
            'price' : 1200
            }
        with self.app.app_context():
            DB.create_all()

    def tearDown(self):
        """ A method that is called after each test. """
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()
    
    
    #### HELPER METHODS #### 
    def user_registration(
            self,
            username="Berry",
            email="berry@berry.com",
            password="A1234a",
            repeat_password="A1234a"
            ):
        """ User registration helper method."""
        data = {
            'username' :username,
            'email':email,
            'password':password,
            'repeat_password':repeat_password
            }
        return self.client().post('/auth/register', data=data)

    def user_logsin(self, email="berry@berry.com", password="A1234a"):
        """User logging in helper method."""
        data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=data)

    def current_list(self, listname="Visiting mum"):
        """Shopping list creation helper method."""
        data = {'listname':listname}
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data=data)
        return res

    #### END OF HELPER METHODS ####

    def test_shoppingitem_successful_creation(self):
        """ Test API can create a shopping item in a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems', 
        headers=dict(Authorization="Bearer " + access_token),
        data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('wheat flour', str(res.data))

    def test_shoppingitem_must_be_created_in_a_shoppinglist(self):
        """ Test API can must create a shopping item in a shopping list. """
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token),
        data=self.shoppingitem)
        self.assertEqual(res.status_code, 404)
        self.assertNotIn('wheat flour', str(res.data))

    def test_duplicate_shoppingitem_creation_fails(self):
        """ Test API cannot create items with same name in one a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('wheat flour', str(res.data))
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data={
            'itemname':'wheat flour',
            'quantity': 12,
            'price' : 1200
        })
        self.assertEqual(res.status_code, 409)

    def test_multiple_shoppingitem_creations_successful(self):
        """ Test API can create many items in one a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems', 
        headers=dict(Authorization="Bearer " + access_token),data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('wheat flour', str(res.data))
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data={
            'itemname':'maize flour',
            'quantity': 12,
            'price' : 1000
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('maize flour', str(res.data))

    def test_get_shoppingitems(self):
        """ Test API can get all shopping items in a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('wheat flour', str(res.data))

    def test_edit_shoppingitem(self):
        """ Test API can edit a shopping item in a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('wheat flour', str(res.data))
        res = self.client().put('/shoppinglists/1/shoppingitems/1',
        headers=dict(Authorization="Bearer " + access_token), data={
            'itemname':'rice',
            'quantity': 10,
            'price' : 1000
            })
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('wheat flour', str(res.data))

    def test_delete_shoppingitem(self):
        """ Test API can delete a shopping item in a shopping list. """
        self.current_list()
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shoppinglists/1/shoppingitems',
        headers=dict(Authorization="Bearer " + access_token), data=self.shoppingitem)
        self.assertEqual(res.status_code, 201)
        self.assertIn('wheat flour', str(res.data))
        res = self.client().delete('/shoppinglists/1/shoppingitems/1',
        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('wheat flour', str(res.data))

if __name__ == '__main__':
    unittest.main()
