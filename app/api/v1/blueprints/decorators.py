from flask import request, abort, g
from functools import wraps
from app.api.v1.models import user
from app import politico

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get the user id from header
        user_id = request.headers.get('UserId')
        print(user_id)
        print(type(user_id))
        current_user = politico.get_user_by_id(user_id)
        g.user = current_user
        return f(*args, **kwargs)
    return wrapper