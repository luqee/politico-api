import datetime
from app.tests.v1 import utils

test_utils = utils.Utils()

def test_party_creation(client):
    test_utils.register_user(client, 'admin')
    login_res = test_utils.login_user(client, 'admin')
    headers = {
        'User Id': login_res.get_json()['data'][0]['user_id']
    }
    response = client.post('api/v1/parties', json=test_utils.PARTIES[0], headers=headers)
    assert response.status_code == 201