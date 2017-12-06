from functools import wraps
from flask import jsonify, request
from app.models import User

def token_auth_required(function):
    
    @wraps(function)
    def _token(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            response = jsonify({
                'message':
                'No token provided!'})
            response.status_code = 500
            return response
        else:
            token = auth_header.split("Bearer ")
            access_token = token[1]
            if access_token:
                user_id = User.decode_auth_token(access_token)
                if not isinstance(user_id, str):
                    user_id = user_id
                else:
                    response = jsonify({'message':user_id})
                    response.status_code = 401
                    return response
            else:
                response = jsonify({
                    'message':
                    'No access token!'})
                response.status_code = 401
                return response
        return function(user_id=user_id, *args, **kwargs)
    return _token