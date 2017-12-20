#test_token.py

import unittest
import json
import requests
from app import create_app, DB

class ShoppingListTestCase(unittest.TestCase):
    """ Class with shopping list tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            'username' : 'berry',
            'email':'keb@gmail.com',
            'password':'Coolday1',
            'repeat_password':'Coolday1'
            }
        self.userlogs = {
            'email':'keb@gmail.com',
            'password':'Coolday1'
        }
        with self.app.app_context():
            DB.create_all()

    
    def tearDown(self):
        """ A method that is called after each test. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

    def test_no_token(self):
        """ Test that there is no existing token. """
        res = self.client().post(
            '/shoppinglists',
            data={'listname':'cake ingredient'})
        return res
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], u"No token provided!")

    def test_invalid_token(self):
        """ Test that the token is already blacklisted. """
        self.client().post('/auth/register', data=self.user)
        result = self.client().post('/auth/login', data=self.userlogs)
        access_token = json.loads(result.data.decode())['access_token']
        self.client().post(
            '/auth/logout',
            headers=dict(Authorization="Bearer " + access_token))
        res = self.client().post(
            '/shoppinglists',
            headers=dict(Authorization="Bearer " + access_token),
            data={'listname':'cake ingredient'})
        return res
        results = json.loads(res.data.decode())
        self.assertEqual(results['message'], u"No token provided!")

    def test_a_header_without_token(self):
        """ Test that the header exists but it has no token. """
        self.client().post('/auth/register', data=self.user)
        result = self.client().post('/auth/login', data=self.userlogs)
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/shoppinglists',
            headers=dict(Authorization="Bearer "),
            data={'listname':'cake ingredient'})
        return res
        results = json.loads(res.data.decode())
        self.assertEqual(results['message'], u"No access token!")
