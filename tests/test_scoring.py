# tests/test_scoring.py
import pytest
import requests

BASE_URL = 'http://scoring:5001'

@pytest.fixture
def setup():
    # Настройка перед тестами, если необходимо
    pass

def test_index_get(setup):
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200

def test_predict_approved(setup):
    data = {
        'Annual_Income': '50000',
        'Age': '30',
        'Num_Bank_Accounts': '2',
        'Outstanding_Debt': '1000'
    }
    response = requests.post(f'{BASE_URL}/predict', json=data)
    assert response.status_code == 200
    assert response.json()['credit_score'] == 1
    assert 'hash_sum' in response.json()

def test_predict_rejected(setup):
    data = {
        'Annual_Income': '20',
        'Age': '25',
        'Num_Bank_Accounts': '1',
        'Outstanding_Debt': '500000'
    }
    response = requests.post(f'{BASE_URL}/predict', json=data)
    assert response.status_code == 200
    assert response.json()['credit_score'] == 0
    assert 'hash_sum' in response.json()

def test_predict_invalid_data(setup):
    data = {
        'Annual_Income': 'invalid',
        'Age': 'invalid',
        'Num_Bank_Accounts': 'invalid',
        'Outstanding_Debt': 'invalid'
    }
    response = requests.post(f'{BASE_URL}/predict', json=data)
    assert response.status_code == 400
    assert 'error' in response.json()

def test_change_model_post(setup):
    data = {
        'fio': 'John Doe'
    }
    response = requests.post(f'{BASE_URL}/change_model', data=data)
    assert response.status_code == 200
    assert 'Model change request sent.' in response.text

def test_change_model_get(setup):
    response = requests.get(f'{BASE_URL}/change_model')
    assert response.status_code == 200
