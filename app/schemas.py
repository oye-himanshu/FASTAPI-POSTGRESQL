from datetime import datetime
from pydantic import BaseModel, ConfigDict


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

    # this config class help to covert sql model to dict
    model_config = ConfigDict(from_attributes=True)
