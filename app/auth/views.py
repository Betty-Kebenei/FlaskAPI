#  /app/auth/views.py

from . import auth
from . import auth as auth_blueprint
from flask import request, jsonify
from app.models import User
import re

@auth.route('/auth/register', methods=['POST', 'GET'])
def register():
    """ API POST user details, thus registering a user. """

    if request.method == 'POST':
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        if username and email and password: 
            if not re.match(r"(?=^.{3,}$)^[A-Za-z0-9_-]*[._-]?[A-Za-z0-9_-]+$", firstname):
                response = jsonify(
                    {'message':'firstname should contain letters, digits and with a min length of 3'}
                    )
                response.status_code = 400
            if not re.match(r"(?=^.{3,}$)^[A-Za-z0-9_-]*[._-]?[A-Za-z0-9_-]+$", lastname):
                response = jsonify(
                    {'message':'lastname should contain letters, digits and with a min length of 3'}
                    )
                response.status_code = 400
            if not re.match(r"(?=^.{3,}$)^[A-Za-z0-9_-]*[._-]?[A-Za-z0-9_-]+$", username):
                response = jsonify(
                    {'message':'Username should contain letters, digits and with a min length of 3'}
                    )
                response.status_code = 400
                return response
            if not re.match(r"^[\w-]+@([\w-]+\.)+[\w]+$", email):
                response = jsonify(
                {'message':'email should contain letters, digits and spaces only: '
                            'valid format = email@email.com'}
                )
                response.status_code = 400
                return response
            if not re.match(r"^(?=.*[a-z])(?=.*[0-9]){6}", password):
                response = jsonify(
                {'message': 'Password must contain: atleast a lowercase letters, atleast a digit, with min-length of 6'}
                )
                response.status_code = 400
                return response
            user = User.query.filter_by(email=email).first()
            if not user:
                if not User.query.filter_by(username=username).first():
                    user = User(
                        firstname=firstname,
                        lastname=lastname,
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    response = jsonify(
                        {'message':'User with email {} successfully registered'.format(user.email)}
                        )
                    response.status_code = 201
                    return response
                else:
                    response = jsonify({'message':'User with that username already exist.'})
                    response.status_code = 409
                    return response
            else:
                response = jsonify({'message':'User with that email already exist.'})
                response.status_code = 409
                return response
        else:
            if not username:
                response = jsonify({'message':'Please provide username!'})
                response.status_code = 400
                return response
            elif not email:
                response = jsonify({'message':'Please provide email!'})
                response.status_code = 400
                return response
            else:
                response = jsonify({'message':'Please provide password!'})
                response.status_code = 400
                return response
    else:
        results = []
        users = User.get_all()
        if users:
            for user in users:
                obj = {
                    'user_id' : user.user_id,
                    'username' : user.username,
                    'firstname' : user.firstname,
                    'lastname' : user.lastname,
                    'email' : user.email
                    }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return {'message':'No users to display'}, 404

@auth.route('/auth/register/<email>', methods=['DELETE'])
def delete_user(email):
    """API can delete a user."""

    user = User.query.filter_by(email=email).first()
    if user:
        if request.method == 'DELETE':
            user.delete()
            response = jsonify({'message':'User with username:{}\
                                successfully deleted'.format(user.username)})
            response.status_code = 202
            return response
    else:
        response = jsonify({'message':'User with email:{} does not exist.'.format(user.email)})
        response.status_code = 404
        return response
    
@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    """ API to login in. """

    if request.method == "POST":
        user = User.query.filter_by(email=request.data['email']).first()
        password = request.data['password']
        if not user and password:
            response = jsonify({
                    'message':
                    'email or password missing!'
                    })
            response.status_code = 400
            return response
        else:
            if user:
                if user.verify_password(password):
                    access_token = user.encode_auth_token(user.user_id)
                    if access_token:
                        response = jsonify({
                            'message':'Hey {} you are successfully logged in.'.format(user.firstname),
                            'access_token': access_token.decode()
                            })
                        response.status_code = 200
                        return response
                else:
                    response = jsonify({
                        'message':
                        'Incorrect password!'
                        .format(user.username)})
                    response.status_code = 404
                    return response
            else:
                response = jsonify({
                    'message':
                    'User does not exist!'
                    })
                response.status_code = 404
                return response
