from flask import Blueprint, request, jsonify
from app.api.v1.models import user
from app import politico
from app.api.v1.blueprints.validator import Validator

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/user/register', methods=['POST'])
def register():
    """ This method registers a user to the application."""
    data = request.get_json()
    user_data = {
        'firstname': data['firstname'],
        'lastname': data['lastname'],
        'email': data['email'],
        'password': data['password'],
        'othername': data['othername'],
        'phone_number': data['phone_number'],
        'is_admin': data['is_admin'],
    }
    if Validator.validate_user(user_data):
        result = politico.register_user(data)
    if result == 'User added':
        # return a response notifying the user that they registered successfully
        response = {
            'status': 201,
            'data':[{'message': 'User registered successfully'}]
        }
        return jsonify(response), 201
    # notify the user that an account with the same email is already registered
    response = {
        'status': 409,
        'error': 'User already exists'
    }
    return jsonify(response), 409

@auth_blueprint.route('/user/login', methods=['POST'])
def login():
    """ This method logs in a user into the application."""
    data = request.get_json()
    
    user_data = {
        'email': data['email'],
        'password': data['password']
    }
    if Validator.validate_user(user_data):
        result = politico.login_user(user_data)
    if result == 'Invalid credentials':
        # notify the user that there was an error.
        response = {
            'status': 401,
            'error': 'Invalid credentials'
        }
        return jsonify(response), 401
    # return a response notifying the user that they logged in successfully
    response_data = {
        'status': 200,
        'data': []
    }
    response_data['data'].append({
        'message': 'Successfull log in',
        'auth_token': result.decode()
    })
    return jsonify(response_data), 200        