from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class CreateUser(BaseUser):
    pass


class UpdateUser(BaseUser):
    pass


class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True


class CreatePost(PostBase):
    pass  # it will inherit all the properties of postbase


class UpdatePost(PostBase):
    pass


#  below code is for defining the response data
class Post(PostBase):
    id: int
    created_at: datetime
    created_by: int
    created_by_details: User

    # this config class help to covert sql model to dict
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
