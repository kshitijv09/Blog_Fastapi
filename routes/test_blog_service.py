import pytest
import requests

# Assuming your FastAPI server is running at this URL
BASE_URL = 'http://localhost:8000'

# Sample blog ID for testing
sample_blog_id = '65ba350733edb786324bc5bf'  # Example blog ID


def test_get_blogs():
    # Make a GET request to the endpoint
    response = requests.get(f'{BASE_URL}/blogs')

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # You can add more assertions to validate the response body if needed


def test_get_blog_by_id():
   
    response = requests.get(f'{BASE_URL}/blogs/{sample_blog_id}')

    assert response.status_code == 200

    expected_keys = ['id', 'title', 'tag', 'content', 'date', 'author']
    assert all(key in response.json() for key in expected_keys)

    # Test for a non-existent blog ID
    non_existent_blog_id = '65bb7dd71f468d91d944b891'
    response = requests.get(f'{BASE_URL}/blogs/{non_existent_blog_id}')

    assert response.status_code == 404

def test_get_blogs_by_user():
    # Define a sample user ID
    sample_user_id = '65bb7bb92f6e37fa81f02915'

    # Make a GET request to the endpoint with the sample user ID
    response = requests.get(f'{BASE_URL}/blogs/{sample_user_id}/blogs')

    # Check if the status code is 200 OK
    assert response.status_code == 200

    non_existent_blog_id = '65bb7dd71f468d91d944b891'
    response = requests.get(f'{BASE_URL}/blogs/{non_existent_blog_id}/blogs')

    assert response.status_code == 404

   

def test_create_blog():
    # Define a sample blog data
    sample_blog_data = {
        'title': 'Sample Blog',
        'tag': 'Technology',
        'content': 'This is a sample blog content.',
        'date': '2024-01-31',
        'author': 'John Doe'
    }

    # Make a POST request to the endpoint with the sample blog data
    response = requests.post(f'{BASE_URL}/blogs/', json=sample_blog_data)

    # Check if the status code is 201 CREATED
    assert response.status_code == 200

    # Check if the response contains the blog ID
    assert 'id' in response.json()

    # Attempt to create a blog with missing data
    invalid_data = {}
    response = requests.post(f'{BASE_URL}/blogs/', json=invalid_data)
    assert response.status_code == 422
    """ assert response.json()['detail'] == "Invalid request. Blog data is missing." """


def test_update_blog():
    # Define a sample blog ID and updated blog data
    sample_blog_id = '65bbad613c966cf16932a34b'
    updated_blog_data = {
        'title': 'Updated Blog Title',
        'tag': 'Science',
        'content': 'This is the updated blog content.',
        'date': '2024-01-31',
        'author': 'Jane Doe'
    }

    # Make a PUT request to the endpoint with the sample blog ID and updated blog data
    response = requests.put(f'{BASE_URL}/blogs/{sample_blog_id}', json=updated_blog_data)

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check if the response message indicates successful update
    assert response.json()['message'] == 'Blog updated successfully'

    # Add more assertions as needed

def test_delete_blog():
    # Define a sample blog ID
    sample_blog_id = '65bbad613c966cf16932a34b'

    # Make a DELETE request to the endpoint with the sample blog ID
    response = requests.delete(f'{BASE_URL}/blogs/{sample_blog_id}')

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check if the response message indicates successful deletion
    assert response.json()['message'] == 'Blog deleted successfully'

if __name__ == '__main__':
    pytest.main()
