import pytest
import requests

BASE_URL = 'http://request-processing:5000'

@pytest.fixture
def setup():
    # Настройка перед тестами, если необходимо
    pass

def test_index_get(setup):
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200

def test_index_post_approved(setup):
    data = {
        'fio': 'John Doe',
        'annual_income': '50000',
        'age': '30',
        'num_bank_accounts': '2',
        'outstanding_debt': '1000'
    }
    response = requests.post(f'{BASE_URL}/', data=data)
    assert response.status_code == 200
    assert 'Поздравляем, вам одобрен кредит' in response.text

def test_index_post_rejected(setup):
    data = {
        'fio': 'Jane Doe',
        'annual_income': '20',
        'age': '25',
        'num_bank_accounts': '1',
        'outstanding_debt': '500000'
    }
    response = requests.post(f'{BASE_URL}/', data=data)
    assert response.status_code == 200
    assert 'Извините, выдача кредита отклонена' in response.text

def test_index_post_error(setup):
    data = {
        'fio': 'Invalid User',
        'annual_income': 'invalid',
        'age': 'invalid',
        'num_bank_accounts': 'invalid',
        'outstanding_debt': 'invalid'
    }
    response = requests.post(f'{BASE_URL}/', data=data)
    assert response.status_code == 200
    assert 'Извините, ваш запрос завершился с ошибкой, вам перезвонит специалист' in response.text
