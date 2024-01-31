from fastapi import APIRouter,HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
from jwt import create_access_token
from config.userdatabase import db
from models.users import User,UserProfileUpdate,UserInterestsUpdate

userRouter=APIRouter()


""" @router.get("/")
def read_root(current_user: User = Depends(get_current_user)):
    return {"data": "Hello World"} """

@userRouter.post('/register')
def create_user(request: User):
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
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


@userRouter.put('/interests/add/{username}')
def add_interests(username: str, request: UserInterestsUpdate):
    # Check if the user exists
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    # Add interests to the user's profile
    db["user_collection"].update_one({"username": username}, {"$addToSet": {"interests": {"$each": request.interests}}})

    return {"message": f"Interests added to user {username} successfully"}

# Remove Interests Route
@userRouter.delete('/interests/remove/{username}')
def remove_interests(username: str, request: UserInterestsUpdate):
    # Check if the user exists
    existing_user = db["user_collection"].find_one({"username": username})
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')

    # Remove interests from the user's profile
    db["user_collection"].update_one({"username": username}, {"$pull": {"interests": {"$in": request.interests}}})

    return {"message": f"Interests removed from user {username} successfully"}
