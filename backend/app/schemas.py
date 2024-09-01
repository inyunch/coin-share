from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    name: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    group_id: Optional[int] = None

    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str
    code: str
    game_id: int

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True

class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    groups: List[Group] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str