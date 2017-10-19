from app import DB, LOGIN_MANAGER

#passlibs is a package dedicated to password hashing.pip
from passlib.apps import custom_app_context as pwd_context

class User(DB.Model):
    """Create a users table."""

    __tablename__ = "users"

    user_id = DB.column(DB.Integer, primary_key=True)
    firstname = DB.column(DB.String(50))
    lastname = DB.column(DB.String(50))
    username = DB.column(DB.String(50), unique=True)
    email = DB.column(DB.String(50), unique=True)
    password_hash = DB.column(DB.String(128))
    shopping_list_id = DB.Column(DB.Integer, DB.ForeignKey('shoppinglists.list_id'))

    def hash_password(self, password):
        """Hash password during signup."""

        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """Validate password during signin."""

        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return "<ShoppingList: {}>".format(self.username)

@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """Set up user_loader."""

    return User.query.get(int(user_id))

class ShoppingList(object):
    """Create a shopping list table"""

    __tablename__ = "shoppinglists"

    list_id = DB.column(DB.Integer, primary_key=True)
    listname = DB.column(DB.String(50), unique=True)
    shopiing_item_id = DB.column(DB.Integer, DB.ForeignKey('shoppingitems.item_id'))
    users = DB.relationship('User', backref='shoppinglist', lazy='dynamic')
    
    def __repr__(self):
        return "<ShoppingList: {}>".format(self.listname)

class ShoppingItems(object):
    """Create a shopping items table."""

    __tablename__ = "shoppingitems"

    item_id = DB.column(DB.Integer, primary_key=True)
    itemname = DB.column(DB.String(50), unique=True)
    quantity = DB.column(DB.Integer(50))
    price = DB.column(DB.Integer(50))
    shoppinglists = DB.relationship('ShoppingList', backref='shoppingitems', lazy='dynamic')

    def __repr__(self):
        return "<ShoppingItems: {}>".format(self.itemname)