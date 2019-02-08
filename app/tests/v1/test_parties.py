from app.tests.v1 import utils

test_utils = utils.Utils()

def test_party_creation(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 201
    assert type(json_data['data']) == list

def test_get_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_party(client, test_utils.PARTIES[1], headers)
    response =client.get('api/v1/parties/1')
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_get_parties(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_parties(client, headers)
    response =client.get('api/v1/parties')
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_update_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = test_utils.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    data = {
        'name': 'New Party'
    }
    response =client.patch('api/v1/parties/1/name', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list

def test_delete_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    response =client.delete('api/v1/parties/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'Party deleted successfully'