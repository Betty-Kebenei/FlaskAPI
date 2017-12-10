[![Build Status](https://travis-ci.org/Betty-Kebenei/FlaskAPI.svg?branch=master)](https://travis-ci.org/Betty-Kebenei/FlaskAPI)
[![Coverage Status](https://coveralls.io/repos/github/Betty-Kebenei/FlaskAPI/badge.svg?branch=master)](https://coveralls.io/github/Betty-Kebenei/FlaskAPI?branch=master)

# Flask Restful API

This is a flask restful API for a shopping lists application; an application that helps users to keep track of their shopping lists. Using this API, a user can register for an account, login, logout; create, edit, view, or delete shopping lists as well as its items.

## Getting Started

### Prerequisites
You need the following installed/setted-up so as to get the software running:

1. Python 2.7

2. Postgresql

3. Flask

4. Flask-Sqlalchemy

### Installing
Clone the repo by running

> git clone https://github.com/Betty-Kebenei/FlaskAPI.git

Navigate to the directory containing the project.

Then run the following command to install other required requirements after cloning:

> pip install -r requirements.txt

## Database Set-up

Create a database for the api and a database for testing in postgres:

Then first set-up the environment {Be sure to replace postgresUsername and dartabaseName}:

> export DATABASE_URL="postgres://postgresUsername@localhost/databasename"

> export SECRET_KEY="write-your-own-secret-key-could-be-some-random-numbers-characters-digits-e.t.c"

> export FLASK_CONFIG=development

> export FLASK_APP=manage.py

> flask db init

> flask db migrate

> flask db upgrade

## Running the tests

Navigate to the root of the application then run:

> export DATABASE_URL="postgres://postgresUsername@localhost/databasename"

> export SECRET_KEY="write-your-own-secret-key-could-be-some-random-numbers-characters-digits-e.t.c"

> nosetests -sv --with-coverage

## Run the application

Navigate to the root of the application

Run the following commands:

> export DATABASE_URL="postgres://postgresUsername@localhost/databasename"

> export SECRET_KEY="write-your-own-secret-key-could-be-some-random-numbers-characters-digits-e.t.c"

> export FLASK_CONFIG=development

> export FLASK_APP=run.py

> flask run

## Endpoints

An endpoint that has public access as false can only be accessed after a token based authentication. 

| METHOD | ENDPOINT | PUBLIC ACCESS | SUMMARY |
| --- | --- | --- | --- |
| **POST** | /auth/register | TRUE | Register a new user |
| **POST** | /auth/login | TRUE | Existing user can login |
| **GET** | /auth/register | TRUE | A user can see all the registered users |
| **DELETE** | /auth/delete_user | FALSE | A user can delete his/her own account |
| **POST** | /home/shoppinglists | FALSE | A user can create a shopping list |
| **GET** | /home/shoppinglists | FALSE | A user can get all the shopping lists |
| **DELETE** | /home/shoppinglists | FALSE | A user can delete all the shopping lists |
| **GET** | /home/shoppinglists/{listid} | FALSE | A user can get a single shopping list by list id |
| **PUT** | /home/shoppinglists/{listid} | FALSE | A user can edit a single shopping list by list id |
| **DELETE** | /home/shoppinglists/{listid} | FALSE | A user can delete a single shopping list by list id |
| **POST** | /home/shoppinglists/{listid}/shoppingitems | FALSE | A user can create a shopping item |
| **GET** | /home/shoppinglists{listid}/shoppingitems | FALSE | A user can get all the shopping items in a shopping list |
| **DELETE** | /home/shoppinglists{listid}/shoppingitems | FALSE | A user can delete all the shopping items in a shopping list |
| **GET** | /home/shoppinglists/{listid}/shoppingitems/{itemid} | FALSE | A user can get a single shopping item by item id |
| **PUT** | /home/shoppinglists/{listid}/shoppingitems/{itemid} | FALSE | A user can edit a single shopping item by item id |
| **DELETE** | /home/shoppinglists/{listid}/shoppingitems/{itemid} | FALSE | A user can delete a single shopping item by item id |



