from flask import current_app
from app import DB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class User(DB.Model):
    """Create a users table."""

    __tablename__ = "users"

    user_id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(50), unique=True)
    email = DB.Column(DB.String(50), unique=True)
    password = DB.Column(DB.String(128))
    shoppinglists = DB.relationship('ShoppingList', backref='ShoppingList.list_id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        """ initilization """
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Validate password during signin."""
        return check_password_hash(self.password, password)
    
    def save(self):
        """ stores user to database """
        DB.session.add(self)
        DB.session.commit()

    @staticmethod
    def get_all():
        """ get all users """
        return User.query.all()

    def delete(self):
        """ deletes user """
        DB.session.delete(self)
        DB.session.commit()

    def encode_auth_token(self, user_id):
        """ Generating an authentication token and returns a string error is expection occurs"""
        try:
            payload = {
                'sub': user_id,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=70)
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the authentication token"""

        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Sorry your token expired, please log in again!'
        except jwt.InvalidTokenError:
            return 'Token invalid, please login again.'

    def __repr__(self):
        return "<User: {}>".format(self.username)

class ShoppingList(DB.Model):
    """Create a shopping list table"""

    __tablename__ = "shoppinglists"

    list_id = DB.Column(DB.Integer, primary_key=True)
    listname = DB.Column(DB.String(50))
    shoppingitems = DB.relationship('ShoppingItems', backref='ShoppingItems.item_id', cascade="all, delete-orphan")
    created_by = DB.Column(DB.Integer, DB.ForeignKey(User.user_id))
    
    def __init__(self, listname, created_by):
        """ initilization """
        self.listname = listname
        self.created_by = created_by

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
    itemname = DB.Column(DB.String(50))
    quantity = DB.Column(DB.Float, nullable=True)
    units = DB.Column(DB.String(50), nullable=True)
    price = DB.Column(DB.Float, nullable=True)
    currency = DB.Column(DB.String(50), nullable=True)
    item_for_list = DB.Column(DB.Integer, DB.ForeignKey(ShoppingList.list_id))

    def __init__(self, itemname, quantity, units, price, currency, item_for_list):
        """ initilization """
        self.itemname = itemname
        self.quantity = quantity
        self.units = units
        self.price = price
        self.currency = currency
        self.item_for_list = item_for_list

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

class BlacklistToken(DB.Model):
    """ Model for already used tokens """

    __tablename__ = "tokens"

    token_id = DB.Column(DB.Integer, primary_key=True)
    token = DB.Column(DB.String(500), unique=True, nullable=False)
    date_blacklisted = DB.Column(DB.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.date_blacklisted = datetime.now()

    def save(self):
        """ stores token to database """
        DB.session.add(self)
        DB.session.commit()

    def __repr__(self):
        return '<token_id: {}>'.format(self.token)