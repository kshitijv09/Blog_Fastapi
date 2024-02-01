from fastapi import APIRouter,HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
from jwt import create_access_token
from config.userdatabase import db
from models.users import User,UserProfileUpdate,UserInterestsUpdate
from bson import ObjectId
userRouter=APIRouter()

@userRouter.post('/register')
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    """ user_object = dict(request) """
    user_object = request.to_dict()
    user_object["password"] = hashed_pass
    user_id = db["user_collection"].insert_one(user_object)
    return {"res": "created"}

@userRouter.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = db["user_collection"].find_one({"username": request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with this {request.username} username')
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Wrong Username or password')
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@userRouter.put('/profile/{username}')
def update_profile(username: str, request: UserProfileUpdate):
    # Check if the user exists
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    # Update user data
    update_data = {k: v for k, v in request.dict(exclude={"email", "password"}).items() if v is not None}

    # Update user data
    db["user_collection"].update_one({"username": username}, {"$set": update_data})

    return {"message": f"Profile for user {username} updated successfully"}

@userRouter.get('/{user_id}')
def get_user_by_id(user_id: str):
    # Check if the user ID is a valid ObjectId
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid user ID: {user_id}')

    # Find the user by user ID
    user = db["user_collection"].find_one({"_id": ObjectId(user_id)})
    
    # If user does not exist, raise HTTPException
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {user_id} not found')
    
    
    # Convert ObjectId to string for JSON serialization
    user = db["user_collection"].find_one({"_id": ObjectId(user_id)})
    
    # If user does not exist, raise HTTPException
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {user_id} not found')
    
    # Convert ObjectId to string for JSON serialization
    user['_id'] = str(user['_id'])

    # Convert ObjectId to string for 'interests' field
    user['interests'] = [{'_id': str(interest['_id']), 'name': interest['name']} for interest in user['interests']]

    # Remove ObjectId from 'email' and 'password' fields
    user.pop('_id', None)
    user.pop('password', None)

    # Return the user
    return user


@userRouter.put('/interests/add/{username}')
def add_interests(username: str, request: UserInterestsUpdate):
    # Check if the user exists
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
    
    print(request)
    # Add interests to the user's profile
    interests_data = request.interests.to_dict()

    # Add interests to the user's profile
    db["user_collection"].update_one({"username": username}, {"$addToSet": {"interests": interests_data}})

    return {"message": f"Interests added to user {username} successfully"}

# Remove Interests Route
@userRouter.delete('/interests/remove/{username}/{interest_id}')
def remove_interest(username: str, interest_id: str):
    # Check if the user exists
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    # Remove the interest from the user's profile based on its ID
    db["user_collection"].update_one({"username": username}, {"$pull": {"interests": {"_id": ObjectId(interest_id)}}})

    return {"message": f"Interest {interest_id} removed from user {username} successfully"}
