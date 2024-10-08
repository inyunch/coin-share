from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
import random
import string
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password, name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()

def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def update_game(db: Session, game_id: int, game: schemas.GameCreate):
    db_game = get_game(db, game_id)
    if db_game is None:
        return None
    for key, value in game.dict().items():
        setattr(db_game, key, value)
    db.commit()
    db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_id: int):
    game = get_game(db, game_id)
    if game:
        db.delete(game)
        db.commit()
    return game

def generate_group_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def create_group(db: Session, group: schemas.GroupCreate):
    group_code = generate_group_code()
    db_group = models.Group(name=group.name, code=group_code, game_id=group.game_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group: schemas.GroupCreate):
    db_group = get_group(db, group_id)
    if db_group is None:
        return None
    db_group.name = group.name
    db_group.game_id = group.game_id
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    group = get_group(db, group_id)
    if group:
        db.delete(group)
        db.commit()
    return group