#  /app/auth/views.py

from . import auth
from . import auth as auth_blueprint
from flask import request, jsonify
from app.models import User

@auth.route('/auth/register', methods=['POST', 'GET'])
def register():
    """ API POST user details, thus registering a user. """

    if request.method == 'POST':
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        user = User.query.filter_by(email=email).first()
        if not user:
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
            response = jsonify({'message':'User with email:{} already exist.'.format(user.email)})
            response.status_code = 409
            return response
    else:
        results = []
        q = request.args.get('q')
        if q:
            users = User.query.filter_by(
                user_id=user_id).filter(User.username.like('%{0}%'.format(q)))
        else:
            users = User.query.filter_by(user_id=user_id)

        if users:
            pagination = users.paginate(page, per_page=limit, error_out=False)
            users = pagination.items
            if pagination.has_prev:
                prev = url_for('auth.register', user_id=user_id, page=page-1, limit= limit, _external=True)
            else:
                prev = None
            if pagination.has_next:
                next = url_for('auth.register', user_id=userid, page=page+1, limit=limit, _external=True)
            else:
                next = None

            for user in users:
                obj = {
                    'user_id' : user.user_id,
                    'username' : user.username,
                    'firstname' : user.firstname,
                    'lastname' : user.lastname,
                    'email' : user.email
                    }
                results.append(obj)
            response = jsonify({
                    'users': results,
                    'prev': prev,
                    'next': next,
                    'count': pagination.total
                    })
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
        password = user.verify_password(request.data['password'])
        if user:
            if password:
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
                    'Hey {} you entered incorrect password!'
                    .format(user.username)})
                response.status_code = 404
                return response
        else:
            response = jsonify({
                'message':
                'Hey no user with such email!'
                })
            response.status_code = 404
            return response
