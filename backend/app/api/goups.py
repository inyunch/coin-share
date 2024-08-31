from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Group, Game
from ..dependencies import role_required
from ..schemas import GroupCreate, GroupResponse

router = APIRouter()

@router.post("/groups/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db), current_user=Depends(role_required(Role.ADMIN, Role.GROUP_ADMIN))):
    db_group = Group(name=group.name, code=group.code, game_id=group.game_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group