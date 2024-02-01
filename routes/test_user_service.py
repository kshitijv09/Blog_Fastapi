# test_user_service.py

import pytest
from bson import ObjectId
from routes.userRoute import create_user, login, update_profile, get_user_by_id, add_interests, remove_interests  # Import your user routes
from mongomock import MongoClient
from oauth import oauth2_scheme
from models.users import User

# Sample data for testing
sample_user_id = str(ObjectId())
sample_user = {
    "_id": ObjectId(sample_user_id),
    "username": "test_user",
    "email": "test@example.com",
    "password": "hashed_password",
    "interests": [
        {"_id": ObjectId(), "name": "interest1"},
        {"_id": ObjectId(), "name": "interest2"}
    ]
}

# Set up and teardown for test database
@pytest.fixture(autouse=True)
def setup_teardown():
    # Set up: Connect to the mock MongoDB database
    client = MongoClient()
    db = client['test_db']  # Change 'test_db' to your desired test database name
    # Set up: Insert sample data into the test database
    user_collection = db['user_collection']  # Change 'user_collection' to your desired test collection name
    user_collection.insert_one(sample_user)
    yield
    # Teardown: Clean up the test database after the tests are completed
    client.drop_database('test_db')  # Drop the test database after tests

# Test cases
def test_create_user():
    # Test creating a new user
    # You can use the requests library or simulate the request directly
    # For simplicity, you can call the function directly and check the return value
    new_user = create_user(User(username="new_user", email="new@example.com", password="password"))
    assert new_user["res"] == "created"

""" def test_login():
    # Test user login
    # You can simulate the request and check the response
    # For simplicity, call the function directly and check the return value
    login_response = login(OAuth2PasswordRequestForm(username="test_user", password="hashed_password"))
    assert "access_token" in login_response
    assert login_response["token_type"] == "bearer" """

# Add more test cases for other user routes (update_profile, get_user_by_id, add_interests, remove_interests)
