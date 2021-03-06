#run.py

import os
from app import create_app

CONFIG_NAME = os.getenv('FLASK_CONFIG')
APP = create_app(CONFIG_NAME)

if __name__ == '__main__':
    APP.run()
