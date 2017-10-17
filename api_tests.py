import unittest
from flask_testing import TestCase
from app import create_app, DB
from app.models import User, ShoppingList, ShoppingItems

class TestBase(TestCase):
    """Testing base class where configurations are set."""
    def create_app(self):
        """A method for passing testing configurations."""
        config_name = 'testing'
        app = create_app(config_name)
        return app

    def setUp(self):
        """A method that will be called before every test."""

        DB.create_all()

    def tearDown(self):
        """A method that will be called after every test"""

        DB.session.remove()
        DB.drop_all()

class TestUser(TestBase):
    """This class represents testing on the user model."""

    def test_user_model_number(self):
        """Test number of users in the user table."""

        #Create a user
        user = User(
            firstname="firstname",
            lastname="lastname",
            username="username",
            email="email@gmail.com",
            password="A123456")

        #save the user to the database
        DB.session.add(user)
        DB.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_user_firstname(self):
        """Test the validation of the firstname:
        The user should not be added because the firstname is invalid"""

        user2 = User(
            firstname="@@@",
            lastname="lastname",
            username="username",
            email="email@gmail.com",
            password="A123456")
        DB.session.add(user2)
        DB.session.commit()
        self.assertNotEqual(User.query.count(), 2)

    def test_user_lastname(self):
        """Test the validation of the lastname:
        The user should not be added because the lastname is invalid"""

        user3 = User(
            firstname="firstname",
            lastname="",
            username="username",
            email="email@gmail.com",
            password="A123456")
        DB.session.add(user3)
        DB.session.commit()
        self.assertNotEqual(User.query.count(), 2)

    def test_user_username(self):
        """Test the validation of the username:
        The user should not be added because the username is invalid"""

        user4 = User(
            firstname="firstname",
            lastname="lastname",
            username="us",
            email="email@gmail.com",
            password="A123456")
        DB.session.add(user4)
        DB.session.commit()
        self.assertNotEqual(User.query.count(), 2)

    def test_user_email(self):
        """Test the validation of the email:
        The user should not be added because the email is invalid"""

        user5 = User(
            firstname="firstname",
            lastname="lastname",
            username="username",
            email="email",
            password="A123456")
        DB.session.add(user5)
        DB.session.commit()
        self.assertNotEqual(User.query.count(), 2)

    def test_user_password(self):
        """Test the validation of the password:
        The user should not be added because the password is invalid"""

        user6 = User(
            firstname="firstname",
            lastname="lastname",
            username="username",
            email="email@gmail.com",
            password="aaaaaa")
        DB.session.add(user6)
        DB.session.commit()
        self.assertNotEqual(User.query.count(), 2)

class TestShoppinglists(TestBase):
    """This class represents testing on the shopping list model."""

    def test_shoppinglist_model_number(self):
        """Test number of shopping lists in the user table."""

        #Create a shopping list
        shopping_list = ShoppingList(listname="Books")
        DB.session.add(shopping_list)
        DB.session.commit()

        self.assertEqual(ShoppingList.query.count(), 1)

    def test_shoppinglist_validation(self):
        """Test the validation of the listname:
        The shopping list should not be added because the listname is invalid"""

        #Create a shopping list
        shopping_list2 = ShoppingList(listname="")
        DB.session.add(shopping_list2)
        DB.session.commit()

        self.assertNotEqual(ShoppingList.query.count(), 2)
        
class ShoppingItemsTestCase(TestBase):
    """This class represents testing on the shopping list model."""

    def test_shoppingitems_model(self):
        """Test number of shopping lists in the user table."""

        #Create a shopping item
        shopping_item = ShoppingItems(itemname="Note book", quantity=2, price=500)
        DB.session.add(shopping_item)
        DB.session.commit()

        self.assertEqual(ShoppingItems.query.count(), 1)

    def test_shoppingitems_itemname(self):
        """Test the validation of the itemname:
        The shopping item should not be added because the itemname is invalid"""

        #Create a shopping item
        shopping_item2 = ShoppingItems(itemname="", quantity=2, price=500)
        DB.session.add(shopping_item2)
        DB.session.commit()

        self.assertNotEqual(ShoppingItems.query.count(), 2)
    
    def test_shoppingitems_quantity(self):
        """Test the validation of the quantity:
        The shopping item should not be added because the quantity is invalid"""

        #Create a shopping item
        shopping_item3 = ShoppingItems(itemname="Note book", quantity="two", price=500)
        DB.session.add(shopping_item3)
        DB.session.commit()

        self.assertNotEqual(ShoppingItems.query.count(), 2)
    
    def test_shoppingitems_price(self):
        """Test the validation of the price:
        The shopping item should not be added because the price is invalid"""

        #Create a shopping item
        shopping_item4 = ShoppingItems(itemname="Note book", quantity=2, price="five hundred")
        DB.session.add(shopping_item4)
        DB.session.commit()

        self.assertNotEqual(ShoppingItems.query.count(), 2)



if __name__ == '__main__':
    unittest.main()
