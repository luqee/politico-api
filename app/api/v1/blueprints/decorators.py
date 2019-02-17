from functools import wraps
from flask import request, abort, g
from app.api.v1.models import user
from app import politico

def login_required(fun):
    ''' Login required decorator'''
    @wraps(fun)
    def wrapper(*args, **kwargs):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            # Attempt to decode the token and get the User ID
            user_id = user.User.decode_token(access_token)
            if not isinstance(user_id, str):
                current_user = politico.get_user_by_id(user_id)
                g.user = current_user
                # Go ahead and handle the request, the user is authenticated
                return fun(*args, **kwargs)       
            abort(401)
    return wrapper
