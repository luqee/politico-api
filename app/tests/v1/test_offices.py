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
        'name': 'New Office'
    }
    response =client.patch('api/v1/offices/1/name', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

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
