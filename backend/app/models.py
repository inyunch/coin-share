from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Role:
    ADMIN = 'admin'
    GROUP_ADMIN = 'group_admin'
    ACCOUNTANT = 'accountant'
    USER = 'user'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=Role.USER)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    users = relationship('User', backref='group', lazy=True)
    game = relationship('Game', backref='groups', lazy=True)

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)