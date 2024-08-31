from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str
    code: str
    game_id: int

class GroupResponse(GroupCreate):
    id: int