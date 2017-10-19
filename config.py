#config.py
import os

class Config(object):
    """Common configurations"""

    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:adams@localhost/api'


class DevelopmentConfig(Config):
    """Configurations used locally: While building the API"""

    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configurations used remotely: When the API is deployed"""

    DEBUG = False

class TestingConfig(Config):
    """Testing configurations"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:adams@localhost/testapi'

#A dictionary that enables the above children configurations
APP_CONFIG = {'development':DevelopmentConfig,
              'production':ProductionConfig,
              'testing':TestingConfig}
