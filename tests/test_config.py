#test_config.py

import unittest
from app import create_app

class ConfigurationsTestCase(unittest.TestCase):
    """Class with testcases for the config module."""

    def test_development_config(self):
        """Testing the development configurations"""
        app = create_app(config_name="development")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['TESTING'] is False)
        self.assertTrue(app.config['SQLALCHEMY_ECHO'] is True)

    def test_production_config(self):
        """Testing the production configurations"""
        app = create_app(config_name="production")
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(app.config['TESTING'] is False)
        self.assertTrue(app.config['SQLALCHEMY_ECHO'] is False)

    def test_testing_config(self):
        """Testing the testing configurations"""
        app = create_app(config_name="testing")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(app.config['SQLALCHEMY_ECHO'] is False)

if __name__ == '__main__':
    unittest.main()
