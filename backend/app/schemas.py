from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str
    name: str
    role: str = 'user'

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    group_id: int = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class GroupBase(BaseModel):
    name: str
    code: str
    game_id: int

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True

class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True