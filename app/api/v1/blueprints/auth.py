from flask import Blueprint, request, jsonify, make_response
from app import politico
from app.api.v1.blueprints.validator import Validator

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_blueprint.route('/user/register', methods=['POST'])
def register():
    """ This method registers a user to the application."""
    data = None
    response = {
        'status': 400,
        'error': 'Provide: firstname, lastname, email, othername, phone_number, and password as json.'
    }
    try:
        data = request.get_json()
    except:
        return jsonify(response), 400

    if not data:
        return jsonify(response), 400

    user_data = {
        'firstname': data.get('firstname'),
        'lastname': data.get('lastname'),
        'email': data.get('email'),
        'password': data.get('password'),
        'othername': data.get('othername'),
        'phone_number': data.get('phone_number'),
        'is_admin': data.get('is_admin'),
        'is_politician': data.get('is_politician')
    }
    valdiator_result = Validator.validate_user(user_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    if isinstance(valdiator_result, bool) and valdiator_result:
        result = politico.register_user(user_data)

    response = {}
    if result == 'User added':
        # return a response notifying the user that they registered successfully
        response['status'] = 201
        response['data'] = []
        response['data'].append({
            'message': 'User registered successfully'
        })
    elif result == 'Other name taken':
        # return a response notifying the user that othername is taken
        response['status'] = 409
        response['error'] = 'The othername you chose is taken'
    elif result == 'User already exists':
        # notify the user that an account with the same email is already registered
        response['status'] = 409
        response['error'] = 'User already exists'
    return make_response(jsonify(response), response['status'])

@auth_blueprint.route('/user/login', methods=['POST'])
def login():
    """ This method logs in a user into the application."""
    data = None
    response = {
        'status': 400,
        'error': 'Provide email and password as json.'
    }
    try:
        data = request.get_json()
    except:
        return jsonify(response), 400

    if not data:
        return jsonify(response), 400

    user_data = {
        'email': data.get('email'),
        'password': data.get('password')
    }
    valdiator_result = Validator.validate_user(user_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    if isinstance(valdiator_result, bool) and valdiator_result:
        result = politico.login_user(user_data)

    response = {}
    if result == 'Invalid credentials':
        # notify the user that there was an error.
        response['status'] = 401
        response['error'] = 'Invalid credentials'
    elif isinstance(result, bytes):
        # return a response notifying the user that they logged in successfully
        response['status'] = 200
        response['data'] = []
        response['data'].append({
            'message': 'Successfull log in',
            'auth_token': result.decode()
        })
    return make_response(jsonify(response), response['status'])
