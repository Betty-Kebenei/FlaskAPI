#test_auth.py

import unittest
import json
from app import create_app, DB
from app.models import User

class UserTestCase(unittest.TestCase):
    """ Class with authentication tests . """

    def setUp(self):
        """ A method that is called before each test. """
        """ Pass testing configuration and initializes the app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            'firstname':'Betty',
            'lastname': 'Kebenei',
            'username' : 'Berry',
            'email':'keb@gmail.com',
            'password':'Coolday1'
            }
        self.userlogs = {
            'email':'keb@gmail.com',
            'password':'Coolday1'
        }
        with self.app.app_context():
            DB.create_all()
    
    def tearDown(self):
        """ A method that is called after each test. """
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

    def test_user_registration(self):
        """ Test API user can register. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], u"User with email keb@gmail.com successfully registered")

    def test_duplicate_registration(self):
        """ Test API user cannot register with an existing email. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        res = self.client().post('/auth/register', data={
            'firstname':'Brillian',
            'lastname': 'Baraka',
            'username' : 'Bri',
            'email':'keb@gmail.com',
            'password':'1Sayhello'
            })
        self.assertEqual(res.status_code, 404)

    def test_delete_user(self):
        """ Test API can delete a user. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        res = self.client().delete('/auth/register/keb@gmail.com')
        self.assertEqual(res.status_code, 202)

    def test_login(self):
        """ Test API user can login. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        results = self.client().post('/auth/login', data=self.userlogs)
        self.assertEqual(results.status_code, 200)
        result = json.loads(results.data.decode())
        self.assertTrue(result['access_token']) 

    def test_unregistered_login(self):
        """ Test API user cannot login before
        registering because there is nothing to 
        compare the pashword with in verify_password method. """

        with self.assertRaises(AttributeError):
            self.client().post('/auth/login', data=self.userlogs)

    def test_wrong_password(self):
        """ Test API user cannot login with a wrong password. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        results = self.client().post('/auth/login', data={'email':'keb@gmail.com', 'password':'helloYou1'})
        self.assertEqual(results.status_code, 404)

if __name__ == '__main__':
    unittest.main()
