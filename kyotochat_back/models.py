from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload

DATABASE_URL = "mysql+aiomysql://root:xxx@localhost/kyotoChat"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    registration_date = Column(DateTime)
    birthday = Column(DateTime)
    gender = Column(String)
    age = Column(Integer)
    chat_logs = relationship("ChatLog", back_populates="user", lazy="joined")

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password)

class Character(Base):
    __tablename__ = "characters"
    character_id = Column(Integer, primary_key=True, index=True)
    character_name = Column(String)
    chat_logs = relationship("ChatLog", back_populates="character", lazy="joined")

class ChatLog(Base):
    __tablename__ = "chat_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    character_id = Column(Integer, ForeignKey("characters.character_id"))
    message = Column(Text)
    send_datetime = Column(DateTime)

    user = relationship("User", back_populates="chat_logs", lazy="joined")
    character = relationship("Character", back_populates="chat_logs", lazy="joined")

class UserCredentials(BaseModel):
    email: str
    password: str
