from app.tests.v1 import utils

test_utils = utils.Utils()

def test_user_register(client):
    response = client.post('api/v1/auth/user/register', json=test_utils.USER)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_user_register_without_email(client):
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': '',
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': False,
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert json_data['error'] == 'Please provide your email'

def test_user_register_existing_email(client):
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': test_utils.USER['email'],
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': False,
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    client.post('api/v1/auth/user/register', json=test_utils.USER)
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert type(json_data['error']) == str
    assert json_data['error'] == 'User already exists'

def test_user_register_taken_othername(client):
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': 'diff@app.com',
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': False,
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    client.post('api/v1/auth/user/register', json=test_utils.USER)
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert type(json_data['error']) == str
    assert json_data['error'] == 'The othername you chose is taken'

def test_user_register_invalid_email(client):
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': 'emailaddress',
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': False,
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'email is invalid'

def test_user_register_invalid_number(client):
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': test_utils.USER['email'],
        # phone number should be 12 digits
        'phone_number': '234435',
        'is_admin': False,
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'phone_number is invalid'

def test_user_register_with_empty_payload(client):
    data = {
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str

def test_user_register_with_no_payload(client):
    response = client.post('api/v1/auth/user/register')
    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str

def test_admin_register(client):
    response = client.post('api/v1/auth/user/register', json=test_utils.ADMIN)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_politician_register(client):
    response = client.post('api/v1/auth/user/register', json=test_utils.POLITICIAN)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_user_login(client):
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['status'] == 200
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'Successfull log in'
    assert json_data['data'][0]['auth_token'] is not None

def test_user_login_with_empty_data(client):
    test_utils.register_user(client, 'user')
    data = {
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide email and password as json.'

def test_user_login_without_data(client):
    test_utils.register_user(client, 'user')
    response = client.post('api/v1/auth/user/login')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide email and password as json.'

def test_user_login_without_email(client):
    test_utils.register_user(client, 'user')
    data = {
        'email': '',
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Please provide your email'

def test_user_login_without_password(client):
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': ''
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Please provide your password'

def test_user_login_with_invalid_email(client):
    test_utils.register_user(client, 'user')
    data = {
        'email': '  erw  ',
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'email is invalid'

def test_user_login_with_invalid_password(client):
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': '  '
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'password is invalid'
