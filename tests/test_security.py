# tests/test_security_service.py

import pytest
import requests
import uuid
from datetime import datetime

BASE_URL = 'http://security:5002'


@pytest.fixture
def setup():
    # Настройка перед тестами, если необходимо
    pass


def test_change_model(setup):
    data = {
        'fio': 'Darya',
        'hash_sum': 'abc123'
    }
    response = requests.post(f'{BASE_URL}/change_model', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Change request received'


def test_apply_change(setup):
    data = {
        'request_id': 'ae599faa-2066-44da-93ba-9caf1b52c560',
        'fio': 'Darya'
    }
    response = requests.post(f'{BASE_URL}/apply_change', data=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Change applied.'


def test_reject_change(setup):
    data = {
        'request_id': '9d3119e2-0f08-4f4a-8de3-aee33e8c762e',
        'fio': 'Darya'
    }
    response = requests.post(f'{BASE_URL}/reject_change', data=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Change rejected.'


def test_validate_success(setup):
    data = {
        'response': {
            'hash_sum': 'abc123'
        }
    }

