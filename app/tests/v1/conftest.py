import pytest
from app import create_app

@pytest.fixture
def client():
    ''' This fixture provides the test client '''
    client = create_app('testing').test_client()
    yield client
