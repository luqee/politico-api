from app.tests.v1 import utils

test_utils = utils.Utils()

def test_user_register(client):
    ''' Test user registration '''
    response = client.post('api/v1/auth/user/register', json=test_utils.USER)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert isinstance(json_data['data'], list)
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_user_register_without_email(client):
    ''' Test user registration without email '''
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
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide your email'

def test_user_register_existing_email(client):
    ''' Test user registration with existing email '''
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
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'User already exists'

def test_user_register_taken_othername(client):
    ''' Test user registration with taken othername '''
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
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The othername you chose is taken'

def test_user_register_invalid_email(client):
    ''' Test user registration with invalid email '''
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
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'email is invalid'

def test_user_register_invalid_number(client):
    ''' Test user registration with invalid number '''
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
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'phone_number is invalid'

def test_user_register_invalid_boolean_is_admin(client):
    ''' Test user registration with invalid type of is_admin '''
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': test_utils.USER['email'],
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': 'False',
        'is_politician': test_utils.USER['is_politician'],
        'password': test_utils.USER['password'],
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'is_admin needs to be boolean'

def test_user_register_invalid_boolean_is_politician(client):
    ''' Test user registration with invalid type of is_politician '''
    data = {
        'firstname': test_utils.USER['firstname'],
        'lastname': test_utils.USER['lastname'],
        'othername': test_utils.USER['othername'],
        'email': test_utils.USER['email'],
        'phone_number': test_utils.USER['phone_number'],
        'is_admin': test_utils.USER['is_admin'],
        'is_politician': 'False',
        'password': test_utils.USER['password'],
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'is_politician needs to be boolean'

def test_user_register_with_empty_payload(client):
    ''' Test user registration with empty payload '''
    data = {
    }
    response = client.post('api/v1/auth/user/register', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)

def test_user_register_with_no_payload(client):
    ''' Test user registration with no payload '''
    response = client.post('api/v1/auth/user/register')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)

def test_admin_register(client):
    ''' Test admin registration '''
    response = client.post('api/v1/auth/user/register', json=test_utils.ADMIN)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert isinstance(json_data['data'], list)
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_politician_register(client):
    ''' Test politician registration '''
    response = client.post('api/v1/auth/user/register', json=test_utils.POLITICIAN)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert isinstance(json_data['data'], list)
    assert json_data['data'][0]['message'] == 'User registered successfully'

def test_user_login(client):
    ''' Test user login '''
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['status'] == 200
    assert isinstance(json_data['data'], list)
    assert json_data['data'][0]['message'] == 'Successfull log in'
    assert json_data['data'][0]['auth_token'] is not None

def test_user_login_invalid_credentials(client):
    ''' Test user login with invalid credentials '''
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': 'wrong'
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['status'] == 401
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Invalid credentials'

def test_user_login_with_empty_data(client):
    ''' Test user login with empty data '''
    test_utils.register_user(client, 'user')
    data = {
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide email and password as json.'

def test_user_login_without_data(client):
    ''' Test user login without payload '''
    test_utils.register_user(client, 'user')
    response = client.post('api/v1/auth/user/login')
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide email and password as json.'

def test_user_login_without_email(client):
    ''' Test user login without email '''
    test_utils.register_user(client, 'user')
    data = {
        'email': '',
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide your email'

def test_user_login_without_password(client):
    ''' Test user login without password '''
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': ''
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide your password'

def test_user_login_with_invalid_email(client):
    ''' Test user login with invalid email '''
    test_utils.register_user(client, 'user')
    data = {
        'email': '  erw  ',
        'password': test_utils.USER['password']
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'email is invalid'

def test_user_login_with_invalid_password(client):
    ''' Test user login with invalid password '''
    test_utils.register_user(client, 'user')
    data = {
        'email': test_utils.USER['email'],
        'password': '  '
    }
    response = client.post('api/v1/auth/user/login', json=data)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'password is invalid'
