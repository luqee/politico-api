from app.tests.v1 import utils

test_utils = utils.Utils()

def test_user_register(client):
    response = client.post('api/v1/auth/user/register', json=test_utils.USER)
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == 201
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'User registered successfully'

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
    assert type(json_data['data'][0]['user_id']) == int