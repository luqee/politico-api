import pytest
from app import create_app

@pytest.fixture
def client():
    client = create_app('testing').test_client()
    yield client