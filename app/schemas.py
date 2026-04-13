from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class DiscussionCreate(BaseModel):
    title: str
    content: str


class DiscussionUpdate(BaseModel):
    title: str
    content: str


class DiscussionResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    discussion_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
