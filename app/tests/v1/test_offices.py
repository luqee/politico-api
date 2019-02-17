from app.tests.v1 import utils

TEST_UTILS = utils.Utils()

def test_create_office(client):
    ''' Test create office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/offices', json=TEST_UTILS.OFFICES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 201
    assert isinstance(json_data['data'], list)

def test_non_admin_create_office(client):
    ''' Test create office by non admin '''
    TEST_UTILS.register_user(client, 'user')
    login_res = TEST_UTILS.login_user(client, 'user')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/offices', json=TEST_UTILS.OFFICES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 403
    assert json_data['status'] == 403
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'You need to be an admin to create an office'

def test_create_duplicate_office(client):
    ''' Test cannot create duplicate office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    client.post('api/v1/offices', json=TEST_UTILS.OFFICES[0], headers=headers)
    response = client.post('api/v1/offices', json=TEST_UTILS.OFFICES[0], headers=headers)
    json_data = response.get_json()
    assert response.status_code == 409
    assert json_data['status'] == 409
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Office exists'

def test_create_office_no_payload(client):
    ''' Test office cannot be created with no payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    response = client.post('api/v1/offices', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_create_office_empty_payload(client):
    ''' Test office cannot be created with empty payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {

    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_create_office_no_name(client):
    ''' Test office cannot be created with no name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '',
        'office_type': TEST_UTILS.OFFICES[0]['office_type'],
        'description': TEST_UTILS.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide the name'

def test_create_office_name_spaces(client):
    ''' Test office cannot be created with space name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': '    ',
        'office_type': TEST_UTILS.OFFICES[0]['office_type'],
        'description': TEST_UTILS.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Please provide a valid name'

def test_create_office_short_name(client):
    ''' Test office cannot be created with short name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'we',
        'office_type': TEST_UTILS.OFFICES[0]['office_type'],
        'description': TEST_UTILS.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The name provided is too short'

def test_create_office_long_name(client):
    ''' Test office cannot be created with long name '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'dilgjdigiceergeruguduergruega',
        'office_type': TEST_UTILS.OFFICES[0]['office_type'],
        'description': TEST_UTILS.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The name provided is too long'

def test_create_office_invalid_type(client):
    ''' Test office cannot be created with invalid office_type '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': TEST_UTILS.OFFICES[0]['name'],
        'office_type': 'notype',
        'description': TEST_UTILS.OFFICES[0]['description']
    }
    response = client.post('api/v1/offices', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'The office_type provided is invalid'
    
def test_get_office(client):
    ''' Test get single office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.get('api/v1/offices/1')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_get_non_existing_office(client):
    ''' Test get non existing office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.get('api/v1/offices/13')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Office not found'

def test_get_offices(client):
    ''' Test get all offices '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_offices(client, headers)
    response = client.get('api/v1/offices')
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_update_office(client):
    ''' Test update single office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    data = {
        'name': 'Prime',
        'office_type': 'State',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
    }
    response = client.patch('api/v1/offices/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 200
    assert isinstance(json_data['data'], list)

def test_update_office_empty_payload(client):
    ''' Test update office with empty payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    data = {
    }
    response = client.patch('api/v1/offices/1', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_update_office_no_payload(client):
    ''' Test update office with no payload '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.patch('api/v1/offices/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == 400
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Provide name, office_type, and description as json'

def test_update_non_existing_office(client):
    ''' Test update non existing office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    data = {
        'name': 'Prime',
        'office_type': 'State',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.patch('api/v1/offices/12', json=data, headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Office not found'

def test_delete_office(client):
    ''' Test delete office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.delete('api/v1/offices/1', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 202
    assert isinstance(json_data['data'], list)
    assert json_data['data'][0]['message'] == 'Office deleted successfully'

def test_delete_non_existing_office(client):
    ''' Test delete non existing office '''
    TEST_UTILS.register_user(client, 'admin')
    login_res = TEST_UTILS.login_user(client, 'admin')
    headers = {
        'Authorization': 'Bearer {0}'.format(login_res.get_json()['data'][0]['auth_token'])
    }
    TEST_UTILS.create_office(client, TEST_UTILS.OFFICES[1], headers)
    response = client.delete('api/v1/offices/9', headers=headers)
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data['status'] == 404
    assert isinstance(json_data['error'], str)
    assert json_data['error'] == 'Office not found'
