from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4

class Interest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str

class User(BaseModel):
    email: str
    password: str
    username: str
    interests: Optional[List[Interest]] = []

class Login(BaseModel):
    username: str
    password: str

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None

class UserInterestsUpdate(BaseModel):
    interests: Interest

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
