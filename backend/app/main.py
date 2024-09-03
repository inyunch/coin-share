from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas, auth
from .database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
import random
import string

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Login attempt for username: {form_data.username}")
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print(f"Authentication failed for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    print(f"Authentication successful for username: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/games", response_model=list[schemas.Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    games = crud.get_games(db, skip=skip, limit=limit)
    return games

@app.post("/games", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_admin)):
    new_game = crud.create_game(db=db, game=game)
    if new_game is None:
        raise HTTPException(status_code=400, detail="Failed to create game")
    return new_game

@app.put("/games/{game_id}", response_model=schemas.Game)
def update_game(game_id: int, game: schemas.GameCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_admin)):
    updated_game = crud.update_game(db, game_id=game_id, game=game)
    if updated_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return updated_game

@app.delete("/games/{game_id}", response_model=schemas.Game)
def delete_game(game_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_admin)):
    game = crud.delete_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@app.get("/groups", response_model=list[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    groups = crud.get_groups(db, skip=skip, limit=limit)
    return groups

@app.post("/groups", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_group_admin)):
    return crud.create_group(db=db, group=group)

@app.put("/groups/{group_id}", response_model=schemas.Group)
def update_group(group_id: int, group: schemas.GroupCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_group_admin)):
    updated_group = crud.update_group(db, group_id=group_id, group=group)
    if updated_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@app.delete("/groups/{group_id}", response_model=schemas.Group)
def delete_group(group_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.check_group_admin)):
    group = crud.delete_group(db, group_id=group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group