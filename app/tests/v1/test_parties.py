from app.tests.v1 import utils

TEST_UTILS = utils.Utils()

def test_party_creation(client):
    ''' Test party can be created '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/parties', json=TEST_UTILS.PARTIES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 201
    assert isinstance(json_data['data'], list)

def test_party_create_duplicate(client):
    ''' Test cannot create duplicate party '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=TEST_UTILS.PARTIES[0], headers=headers)
    response = client.post('api/v1/parties', json=TEST_UTILS.PARTIES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Party exists'

def test_party_create_no_payload(client):
    ''' Test create party with no payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/parties', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_party_create_empty_payload(client):
    ''' Test create party with empty payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_party_create_no_name(client):
    ''' Test create party with no name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '',
        'hq_address': TEST_UTILS.PARTIES[0]['hq_address'],
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide the name'

def test_party_create_empty_name(client):
    ''' Test create party with empty name'''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '  ',
        'hq_address': TEST_UTILS.PARTIES[0]['hq_address'],
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide a valid name'

def test_party_create_short_name(client):
    ''' Test create party with short name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'er',
        'hq_address': TEST_UTILS.PARTIES[0]['hq_address'],
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The name provided is too short'

def test_party_create_long_name(client):
    ''' Test create party with long name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'erfdgthytjtyjtyycrfetfesgtergsdg',
        'hq_address': TEST_UTILS.PARTIES[0]['hq_address'],
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The name provided is too long'

def test_party_create_empty_address(client):
    ''' Test create party with no payload'''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': TEST_UTILS.PARTIES[0]['name'],
        'hq_address': '  ',
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide a valid hq_address'

def test_party_create_short_address(client):
    ''' Test create party with short address'''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': TEST_UTILS.PARTIES[0]['name'],
        'hq_address': 'io',
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The hq_address provided is too short'

def test_party_create_long_address(client):
    ''' Test create party with long address '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': TEST_UTILS.PARTIES[0]['name'],
        'hq_address': 'iojgjuyjfytdrdtgjyfujujfyuuyfyhfjdjwfer',
        'logo_url': TEST_UTILS.PARTIES[0]['logo_url'],
        'description': TEST_UTILS.PARTIES[0]['description']
    }
    response = client.post('api/v1/parties', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The hq_address provided is too long'

def test_get_party(client):
    ''' Test get single party '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_party(client, TEST_UTILS.PARTIES[1], headers)
    response = client.get('api/v1/parties/1')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_get_non_existing_party(client):
    ''' Test get non existing party '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_party(client, TEST_UTILS.PARTIES[1], headers)
    response = client.get('api/v1/parties/78')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Party not found'

def test_get_parties(client):
    ''' Test get all parties '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_parties(client, headers)
    response = client.get('api/v1/parties')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_update_party(client):
    ''' Test update party '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = TEST_UTILS.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    data = {
        'name': 'New Party',
        'hq_address': 'Lon Road',
        'logo_url': 'url/to/logo.jpg',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
    }
    response = client.patch('api/v1/parties/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)


def test_update_party_no_data(client):
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = TEST_UTILS.PARTIES[0]
    client.post('api/v1/parties', json=test_party, headers=headers)
    response =client.patch('api/v1/parties/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Provide name, hq_address, logo_url and description as json.'

def test_update_party_empty_data(client):
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = TEST_UTILS.PARTIES[0]
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
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    test_party = TEST_UTILS.PARTIES[0]
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
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=TEST_UTILS.PARTIES[0], headers=headers)
    req_response = client.delete('api/v1/parties/1', headers=headers)
    json_data = req_response.get_json()
    assert req_response.status_code == 202
    assert type(json_data['data']) == list
    assert json_data['data'][0]['message'] == 'Party deleted successfully'

def test_delete_non_existing_party(client):
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/parties', json=TEST_UTILS.PARTIES[0], headers=headers)
    req_response = client.delete('api/v1/parties/7', headers=headers)
    json_data = req_response.get_json()
    assert req_response.status_code == 404
    assert json_data['status'] == 404
    assert type(json_data['error']) == str
    assert json_data['error'] == 'Party not found'
