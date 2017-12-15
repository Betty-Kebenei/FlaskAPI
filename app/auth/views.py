#  /app/auth/views.py

from . import auth
from . import auth as auth_blueprint
from flask import request, jsonify
from app.models import User, BlacklistToken
from app.token_authentication import token_auth_required
import re

@auth.route('/')
@auth.route('/auth/register', methods=['POST', 'GET'])
def register():
    """ API POST user details, thus registering a user. """

    if request.method == 'POST':
        username = str(request.data['username']).lower()
        email = str(request.data['email']).lower()
        password = request.data['password']
        repeat_password = request.data['repeat_password']

        if username and email and password and repeat_password: 
            if not re.match(r"(?=^.{3,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", username):
                response = jsonify(
                    {'message':'Username should contain letters, digits and with a min length of 3'}
                    )
                response.status_code = 400
                return response
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                response = jsonify(
                {'message':
                'Invalid email! A valid email should contain letters, digits, underscores, hyphens and decimals. e.g me.name@kenya.co.ke'}
                )
                response.status_code = 400
                return response
            if not re.match(r"^(?=.*[a-z])(?=.*[0-9]){6}", password):
                response = jsonify(
                {'message': 'Password must contain: atleast a lowercase letters, atleast a digit, with min-length of 6'}
                )
                response.status_code = 400
                return response
            if repeat_password != password:
                response = jsonify({
                    'message':
                    'Password must match'
                    })
                response.status_code = 400
                return response
            user = User.query.filter_by(email=email).first()
            if not user:
                if not User.query.filter_by(username=username).first():
                    user = User(
                        username=username,
                        email=email,
                        password=password,
                        repeat_password=repeat_password
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
                    'email' : user.email
                    }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            response = jsonify({'message':'No users to display!'})
            response.status_code = 404
            return response

@auth.route('/auth/login', methods=['POST'])
def login():
    """ API to login in. """

    user = User.query.filter_by(email=request.data['email']).first()
    password = request.data['password']
    if user and password:
        if user.verify_password(password):
            access_token = user.encode_auth_token(user.user_id)
            if access_token:
                response = jsonify({
                    'message':'Hey {} you are successfully logged in.'.format(user.username),
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
            'email or password missing!'
            })
        response.status_code = 400
        return response

@auth.route('/auth/delete_user', methods=['DELETE'])
@token_auth_required
def delete_user(user_id):
    """API can delete a user."""

    users = User.query.filter_by(user_id=user_id)
    for user in users:
        if user.user_id == user_id:
            user.delete()
            response = jsonify(
                {'message':
                'Account with username:{} successfully deleted'.format(user.username)})
            response.status_code = 202
            return response

@auth.route('/auth/logout', methods=['POST'])
def logout():
    """API can logout a user."""
    
    #Token retrival
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        response = jsonify({
            'message':
            'No token provided!'})
        response.status_code = 500
        return response
    else:
        token = auth_header.split(" ")
        access_token = token[1]
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                invalid_token = BlacklistToken(access_token)
                invalid_token.save()
                response = jsonify(
                    {
                        'message':
                        'You have successfully logged out'
                    }
                )
                response.status_code = 200
                return response

            else:
                response = jsonify({'message':user_id})
                response.status_code = 401
                return response
        else:
            response = jsonify(
                    {
                        'message':
                        'Invalid token'
                    }
                )
            response.status_code = 401
            return response