# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import APP_CONFIG

# db variable initialization
# object that will interact with the database
DB = SQLAlchemy()

def create_app(config_name):
    """Function that takes a configuration name from config.py and loads the right configuration"""
    app = Flask(__name__, instance_relative_config=True) #initiliaze the app
    app.config.from_object(APP_CONFIG[config_name])
    app.config.SECRET_KEY = "qwertykeyboard9876%"
    DB.init_app(app)

    return app
