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

def test_party_create_duplicate(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    response = client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Party exists'

def test_party_create_no_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/parties', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_party_create_empty_payload(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_party_create_no_name(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '',
        'hq_address': test_utils.PARTIES[0]['hq_address'],
        'logo_url': test_utils.PARTIES[0]['logo_url'],
        'description': test_utils.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Please provide the name'

def test_party_create_empty_name(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '  ',
        'hq_address': test_utils.PARTIES[0]['hq_address'],
        'logo_url': test_utils.PARTIES[0]['logo_url'],
        'description': test_utils.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Please provide a valid name'

def test_party_create_invalid_name(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'er',
        'hq_address': test_utils.PARTIES[0]['hq_address'],
        'logo_url': test_utils.PARTIES[0]['logo_url'],
        'description': test_utils.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'The name provided is too short'

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

def test_get_non_existing_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_utils.create_party(client, test_utils.PARTIES[1], headers)
    response =client.get('api/v1/parties/78')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Party not found'

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
        'name': 'New Party',
        'hq_address': 'Lon Road',
        'logo_url': 'url/to/logo.jpg',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    response =client.patch('api/v1/parties/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert type(json_data['data']) == list


def test_update_party_no_data(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = test_utils.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    response =client.patch('api/v1/parties/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_update_party_empty_data(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = test_utils.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    data = {
    }
    response =client.patch('api/v1/parties/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_update_non_existing_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = test_utils.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    data = {
        'name': 'New data',
        'hq_address': 'Lon Road',
        'logo_url': 'url/to/logo.jpg',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    response =client.patch('api/v1/parties/13', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Party not found'

def test_delete_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    req_response =client.delete('api/v1/parties/1', headers=headers)
    json_data = req_response.get_json()
    assert req_response.status_code == 202
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'Party deleted successfully'

def test_delete_non_existing_party(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    req_response =client.delete('api/v1/parties/7', headers=headers)
    json_data = req_response.get_json()
    assert req_response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Party not found'