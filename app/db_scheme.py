from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, conlist
from typing import List


class UserBaseSchema(BaseModel):
    name: str
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class PostSchema(BaseModel):
    title: str
    body: str
    likes: List[str] = []
    dislikes: List[str] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreatePostSchema(PostSchema):
    user: str | None = None
    pass


class PostResponseSchema(PostSchema):
    user: str
    id: str
    pass


class PostResponse(BaseModel):
    status: str
    post: PostResponseSchema


class GetPostSchema(BaseModel):
    id: str
    pass


class EditPostSchema(PostSchema):
    user: str | None = None
    likes: List[str] = []
    dislikes: List[str] = []
    id: str
    pass


class DeletePostSchema(BaseModel):
    id: str
    pass


class AddLikeSchema(BaseModel):
    id: str
    pass


class AddDislikeSchema(BaseModel):
    id: str
    pass


# class UserActionToRedis:
#     user_id: str
#     post_id: str
#     action: str
#     time = datetime.now()
#
#     def __init__(self, user_id: str, action: str, post_id: str):
#         self.user_id = user_id
#         self.action = action
#         self.post_id = post_id

