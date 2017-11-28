import os
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import DB, create_app


app = create_app(config_name=os.getenv('APP_CONFIG'))
migrate = Migrate(app, DB)
manager = Manager(app)

manager.add_command('DB', MigrateCommand)

if __name__ == '__main__':
    manager.run()