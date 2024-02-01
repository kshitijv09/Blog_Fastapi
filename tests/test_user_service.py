import pytest
import requests

sample_user_id = '65ba89fae4f3d866691f0967' 
sample_user_name = 'test@example.com'
BASE_URL = 'http://localhost:8000'

def test_get_user_by_id():
    response = requests.get(f'{BASE_URL}/users/{sample_user_id}')
    assert response.status_code == 200

def test_create_user():
    sample_user_data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    }
    response = requests.post(f'{BASE_URL}/users/register', json=sample_user_data)
    assert response.status_code == 200
    assert response.json()['res'] == 'created'
    invalid_data = {}
    response = requests.post(f'{BASE_URL}/register', json=invalid_data)
    assert response.status_code == 404

def test_login():
    sample_login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    response = requests.post(f'{BASE_URL}/users/login', data=sample_login_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    invalid_credentials = {
        'username': 'invalid_user',
        'password': 'invalid_password'
    }
    response = requests.post(f'{BASE_URL}/login', data=invalid_credentials)
    assert response.status_code == 404

def test_update_profile():
    sample_update_data = {
        'username': 'test@example.com'
    }
    sample_user_name = "test_user"
    response = requests.put(f'{BASE_URL}/users/profile/{sample_user_name}', json=sample_update_data)
    assert response.status_code == 200
    assert response.json()['message'] == f'Profile for user {sample_user_name} updated successfully'

def test_add_interests():
    sample_interest_data = {
        'interests': {
            'name': 'interest_name'
        }
    }
    response = requests.put(f'{BASE_URL}/users/interests/add/{sample_user_name}', json=sample_interest_data)
    assert response.status_code == 200
    assert response.json()['message'] == f'Interests added to user {sample_user_name} successfully'

def test_remove_interests():
    sample_interest_id = '65bbd1d37c3b6f8c88933939'
    sample_username = 'test@example.com'
    response = requests.delete(f'{BASE_URL}/users/interests/remove/{sample_username}/{sample_interest_id}')
    assert response.status_code == 200
    assert response.json()['message'] == f'Interest {sample_interest_id} removed from user {sample_username} successfully'

if __name__ == '__main__':
    pytest.main()
