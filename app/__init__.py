# app/__init__.py
from config import APP_CONFIG
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# variable initializations
DB = SQLAlchemy()
LOGIN_MANAGER = LoginManager()

def create_app(config_name):
    """Function that takes a configuration name from config.py and loads the right configuration"""
    app = FlaskAPI(__name__, instance_relative_config=True) #initiliaze the app
    app.config.from_object(APP_CONFIG[config_name])
    app.config.SECRET_KEY = "qwertykeyboard9876%"
    DB.init_app(app)

    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_message = "Log in first in order to gain access to this page."
    LOGIN_MANAGER.login_view = "login"
        
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
