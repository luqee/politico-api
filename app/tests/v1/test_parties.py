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