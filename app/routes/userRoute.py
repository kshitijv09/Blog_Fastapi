from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import create_access_token
from bson import ObjectId

from hashing import Hash
from config.userdatabase import db
from app.models.users import User, UserProfileUpdate, UserInterestsUpdate

userRouter = APIRouter()

@userRouter.post('/register')
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    user_object = request.to_dict()
    user_object["password"] = hashed_pass
    db["user_collection"].insert_one(user_object)
    return {"res": "created"}

@userRouter.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = db["user_collection"].find_one({"username": request.username})
    if not user or not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Wrong Username or password')
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@userRouter.put('/profile/{username}')
def update_profile(username: str, request: UserProfileUpdate):
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    update_data = {k: v for k, v in request.dict(exclude={"email", "password"}).items() if v is not None}
    db["user_collection"].update_one({"username": username}, {"$set": update_data})

    return {"message": f"Profile for user {username} updated successfully"}

@userRouter.get('/{user_id}')
def get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid user ID: {user_id}')

    user = db["user_collection"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {user_id} not found')

    user['_id'] = str(user['_id'])
    user['interests'] = [{'_id': str(interest['_id']), 'name': interest['name']} for interest in user['interests']]
    user.pop('password', None)

    return user

@userRouter.put('/interests/add/{username}')
def add_interests(username: str, request: UserInterestsUpdate):
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
    
    interests_data = request.interests.to_dict()
    db["user_collection"].update_one({"username": username}, {"$addToSet": {"interests": interests_data}})

    return {"message": f"Interests added to user {username} successfully"}

@userRouter.delete('/interests/remove/{username}/{interest_id}')
def remove_interest(username: str, interest_id: str):
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    db["user_collection"].update_one({"username": username}, {"$pull": {"interests": {"_id": ObjectId(interest_id)}}})

    return {"message": f"Interest {interest_id} removed from user {username} successfully"}
