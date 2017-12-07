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

    def current_list(self, listname="mashujaa day"):
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

    def test_shoppinglist_creation_is_successful(self):
        """ Test API can create a shopping list. """
        res = self.current_list()
        self.assertEqual(res.status_code, 201)
        self.assertIn('mashujaa day', str(res.data))

    def test_duplicate_shoppinglist_creation_fails(self):
        """ Test API can check if a shopping list already exists. """
        res = self.current_list()
        self.assertEqual(res.status_code, 201)
        self.assertIn('mashujaa day', str(res.data))
        res = self.current_list()
        self.assertEqual(res.status_code, 409)

    def test_listname_validation(self):
        """ Test API can check if the listname is validated. """
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'@@@'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"listname should contain letters, digits and with a min length of 3")

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
        self.assertIn('mashujaa day', str(res.data))

    def test_edit_shoppinglist(self):
        """ Test API can edit a shopping list. """
        self.user_registration()
        result = self.user_logsin()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'cake ingredient'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('cake ingredient', str(res.data))
        res = self.client().put(
            '/home/shoppinglists/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'snacks'})
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('cake ingredient', str(res.data))

    def test_delete_shoppinglist(self):
        """ Test API can delete a shopping list. """
        self.user_registration()
        result = self.user_logsin()
        self.assertEqual(result.status_code, 200)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/home/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'snacks'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('snacks', str(res.data))
        res = self.client().delete(
            '/home/shoppinglists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('snacks', str(res.data))
        
if __name__ == '__main__':     
    unittest.main()
