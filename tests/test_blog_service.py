import pytest
import requests

BASE_URL = 'http://localhost:8000'
sample_blog_id = '65ba350733edb786324bc5bf'

def test_get_blogs():
    response = requests.get(f'{BASE_URL}/blog')
    assert response.status_code == 200

def test_get_blog_by_id():
    response = requests.get(f'{BASE_URL}/blog/{sample_blog_id}')
    assert response.status_code == 200
    expected_keys = ['id', 'title', 'tag', 'content', 'date', 'author']
    assert all(key in response.json() for key in expected_keys)
    non_existent_blog_id = '65bb7dd71f468d91d944b891'
    response = requests.get(f'{BASE_URL}/blog/{non_existent_blog_id}')
    assert response.status_code == 404

def test_get_blogs_by_user():
    sample_user_id = '65bb7bb92f6e37fa81f02915'
    response = requests.get(f'{BASE_URL}/blog/{sample_user_id}')
    assert response.status_code == 200
    non_existent_blog_id = '65bb7dd71f468d91d944b891'
    response = requests.get(f'{BASE_URL}/blog/{non_existent_blog_id}')
    assert response.status_code == 404

def test_create_blog():
    sample_blog_data = {
        'title': 'Sample Blog',
        'tag': 'Technology',
        'content': 'This is a sample blog content.',
        'date': '2024-01-31',
        'author': 'John Doe'
    }
    response = requests.post(f'{BASE_URL}/blog', json=sample_blog_data)
    assert response.status_code == 201
    assert 'id' in response.json()
    invalid_data = {}
    response = requests.post(f'{BASE_URL}/blog', json=invalid_data)
    assert response.status_code == 422

def test_update_blog():
    sample_blog_id = '65bbad613c966cf16932a34b'
    updated_blog_data = {
        'title': 'Updated Blog Title',
        'tag': 'Science',
        'content': 'This is the updated blog content.',
        'date': '2024-01-31',
        'author': 'Jane Doe'
    }
    response = requests.put(f'{BASE_URL}/blog/{sample_blog_id}', json=updated_blog_data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Blog updated successfully'

def test_delete_blog():
    sample_blog_id = '65bbad613c966cf16932a34b'
    response = requests.delete(f'{BASE_URL}/blog/{sample_blog_id}')
    assert response.status_code == 200
    assert response.json()['message'] == 'Blog deleted successfully'

if __name__ == '__main__':
    pytest.main()
