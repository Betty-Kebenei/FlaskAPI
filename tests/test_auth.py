#test_auth.py

import unittest
import json
from app import create_app, DB

class AuthenticationTestCase(unittest.TestCase):
    """ Class with authentication tests . """

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
        """ Undoing what setUP did. """
        with self.app.app_context():
            DB.session.remove()
            DB.drop_all()

    def test_successful_user_registration(self):
        """ Test API user can register. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], u"User with email keb@gmail.com successfully registered")

    def test_duplicate_emails_for_registration_fails(self):
        """ Test API user cannot register with an existing email. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        res = self.client().post('/auth/register', data={
            'username' : 'bri',
            'email':'keb@gmail.com',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
            })
        self.assertEqual(res.status_code, 409)

    def test_username_should_be_unique(self):
        """ Test API user cannot register with an existing username. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        res = self.client().post('/auth/register', data={
            'username' : 'berry',
            'email':'berry@gmail.com',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
            })
        self.assertEqual(res.status_code, 409)

    def test_username_is_invalid_for_registration(self):
        """ Test username validation """
        res = self.client().post('/auth/register', data={
            'username' : '&&&',
            'email':'keb@gmail.com',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Username must contain atleast letter; plus other letters or digits and with a min length of 3")
        res = self.client().post('/auth/register', data={
            'username':'',
            'email':'keb@gmail.com',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide username!")
        

    def test_email_is_invalid__for_registration(self):
        """ Test email validation """
        res = self.client().post('/auth/register', data={
            'username' : 'bri',
            'email':'keb',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Invalid email! A valid email should contain letters, digits, underscores, hyphens and decimals. e.g me.name@kenya.co.ke")
        res = self.client().post('/auth/register', data={
            'username':'bri',
            'email':'',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide email!")

    def test_password_is_invalid__for_registration(self):
        """ Test password validation """
        res = self.client().post('/auth/register', data={
            'username' : 'bri',
            'email':'keb@gmail.com',
            'password':'123',
            'repeat_password':'1Sayhello'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Password must contain: atleast a lowercase letters, atleast a digit, with min-length of 6")
        res = self.client().post('/auth/register', data={
            'username':'bri',
            'email':'keb@gmail.com',
            'password':'',
            'repeat_password':''
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Please provide password!")

    def test_password_match_repeat_password(self):
        """ Test password match """
        res = self.client().post('/auth/register', data={
            'username' : 'bri',
            'email':'keb@gmail.com',
            'password':'1Sayhello',
            'repeat_password':'1Sayhello1'
        })
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            u"Password must match")

    def test_login(self):
        """ Test API user can login. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        results = self.client().post('/auth/login', data=self.userlogs)
        self.assertEqual(results.status_code, 200)
        result = json.loads(results.data.decode())
        self.assertTrue(result['access_token']) 

    def test_no_login_inputs_provided(self):
        """ Test API user must provide login information. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        results = self.client().post('/auth/login', data={
            'email':'',
            'password':''  
        })
        self.assertEqual(results.status_code, 400)
        result = json.loads(results.data.decode())
        self.assertEqual(
            result['message'],
            u"email or password missing!")

    def test_get_user(self):
        """ Test API can get users. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        results = self.client().get('/auth/register')
        self.assertEqual(results.status_code, 200)
        

    def test_no_user_found(self):
        """ Test API can capture no users found. """
        results = self.client().get('/auth/register')
        self.assertEqual(results.status_code, 404)
        result = json.loads(results.data.decode())
        self.assertEqual(
            result['message'],
            u"No users to display!")

    def test_delete_user(self):
        """ Test API can delete a user. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        results = self.client().post('/auth/login', data=self.userlogs)
        self.assertEqual(results.status_code, 200)
        access_token = json.loads(results.data.decode())['access_token']
        res = self.client().delete('/auth/delete_user',
        headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 202)

    def test_wrong_password(self):
        """ Test API cannot login user with a wrong password. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail.com', str(res.data))
        results = self.client().post('/auth/login', data={'email':'keb@gmail.com', 'password':'helloYou1'})
        self.assertEqual(results.status_code, 404)

    def test_logout(self):
        """ Test API can logout user. """
        res = self.client().post('/auth/register', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('keb@gmail', str(res.data))
        results = self.client().post('/auth/login', data=self.userlogs)
        self.assertEqual(results.status_code, 200)
        access_token = json.loads(results.data.decode())['access_token']
        response = self.client().post(
            '/auth/logout',
            headers=dict(Authorization="Bearer " + access_token))  
        self.assertEqual(results.status_code, 200)

if __name__ == '__main__':
    unittest.main()
