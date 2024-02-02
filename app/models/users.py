from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from bson import ObjectId

class Interest(BaseModel):
    id: str = Field(default_factory=ObjectId, alias="_id")
    name: str

    def to_dict(self):
        return {
            "_id": ObjectId(self.id),
            "name": self.name
        }

class User(BaseModel):
    email: str
    password: str
    username: str
    interests: Optional[List[Interest]] = []

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "username": self.username,
            "interests": [interest.to_dict() for interest in self.interests]
        }

class Login(BaseModel):
    username: str
    password: str

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None

class UserInterestsUpdate(BaseModel):
    interests: Interest

    def to_dict(self):
        return {
            "interests": self.interests
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
