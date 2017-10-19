from app import DB, LOGIN_MANAGER

#passlibs is a package dedicated to password hashing.pip
from passlib.apps import custom_app_context as pwd_context

class User(DB.Model):
    """Create a users table."""

    __tablename__ = "users"

    user_id = DB.Column(DB.Integer, primary_key=True)
    firstname = DB.Column(DB.String(50))
    lastname = DB.Column(DB.String(50))
    username = DB.Column(DB.String(50), unique=True)
    email = DB.Column(DB.String(50), unique=True)
    password_hash = DB.Column(DB.String(128))
    # shopping_list_id = DB.Column(DB.Integer, DB.ForeignKey('shoppinglists.list_id'))

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

class ShoppingList(DB.Model):
    """Create a shopping list table"""

    __tablename__ = "shoppinglists"

    list_id = DB.Column(DB.Integer, primary_key=True)
    listname = DB.Column(DB.String(50), unique=True)
    # shopping_item_id = DB.Column(DB.Integer, DB.ForeignKey('shoppingitems.item_id'))
    # users = DB.relationship('User', backref='ShoppingList', lazy='dynamic')
    
    def __init__(self, listname):
        """ initilization """
        self.listname = listname

    def save(self):
        """ stores list to database """
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def get_all():
        """ get all shopping lists """
        return ShoppingList.query.all()
    
    def delete(self):
        """ deletes shopping list """
        DB.session.delete(self)
        DB.session.commit()

    def __repr__(self):
        return "<ShoppingList: {}>".format(self.listname)

class ShoppingItems(DB.Model):
    """Create a shopping items table."""

    __tablename__ = "shoppingitems"

    item_id = DB.Column(DB.Integer, primary_key=True)
    itemname = DB.Column(DB.String(50), unique=True)
    quantity = DB.Column(DB.Integer)
    price = DB.Column(DB.Integer)
    # shoppinglists = DB.relationship('ShoppingList', backref='shoppingitems', lazy='dynamic')

    def __init__(self, itemname, quantity, price):
        """ initilization """
        self.itemname = itemname
        self.quantity = quantity
        self.price = price

    def save(self):
        """ stores item to database """
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def get_all():
        """ get all shopping items """
        return ShoppingItems.query.all()
    
    def delete(self):
        """ deletes shopping items """
        DB.session.delete(self)
        DB.session.commit()


    def __repr__(self):
        return "<ShoppingItems: {}>".format(self.itemname)
