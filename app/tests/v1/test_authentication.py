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
