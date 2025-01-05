import pytest
import requests

BASE_URL = 'http://history-of-requests:5003'

@pytest.fixture
def setup():
    # Настройка перед тестами, если необходимо
    pass

def test_add_to_history(setup):
    data = {
        'request_id': '12345',
        'fio': 'John Doe',
        'hash_sum': 'abc123',
        'validation_status': 'Success'
    }
    response = requests.post(f'{BASE_URL}/add_to_history', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Log entry added'

def test_add_to_history_invalid_data(setup):
    data = {
        'invalid_field': 'invalid_value'
    }
    response = requests.post(f'{BASE_URL}/add_to_history', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Log entry added'

def test_add_to_history_empty_data(setup):
    data = {}
    response = requests.post(f'{BASE_URL}/add_to_history', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Log entry added'
