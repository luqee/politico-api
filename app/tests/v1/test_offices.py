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