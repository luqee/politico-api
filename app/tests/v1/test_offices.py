from app.tests.v1 import utils

test_utils = utils.Utils()

def test_create_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/offices', json=test_utils.OFFICES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 201
    assert type(json_data['data']) == list

def test_create_duplicate_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/offices', json=test_utils.OFFICES[0], headers=headers)
    response = client.post('api/v1/offices', json=test_utils.OFFICES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Office exists'

def test_create_office_no_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/offices', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_create_office_empty_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {

    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_create_office_no_name(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '',
        'office_type': test_utils.OFFICES[0]['office_type'],
        'description': test_utils.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Please provide the name'

def test_create_office_invalid_name(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'we',
        'office_type': test_utils.OFFICES[0]['office_type'],
        'description': test_utils.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'The name provided is too short'


def test_get_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    response =client.get('api/v1/offices/1')
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_get_offices(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_offices(client, headers)
    response =client.get('api/v1/offices')
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_update_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    data = {
        'name': 'Prime',
        'office_type': 'State',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
    }
    response =client.patch('api/v1/offices/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_update_office_empty_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    data = {
    }
    response =client.patch('api/v1/offices/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_update_office_no_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    response =client.patch('api/v1/offices/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_update_non_existing_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'Prime',
        'office_type': 'State',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    response =client.patch('api/v1/offices/12', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Office not found'

def test_delete_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    response =client.delete('api/v1/offices/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 202
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'Office deleted successfully'

def test_delete_non_existing_office(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_office(client, test_utils.OFFICES[1], headers)
    response =client.delete('api/v1/offices/9', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Office not found'