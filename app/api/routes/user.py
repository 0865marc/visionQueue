import os

from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.user import User
from app.schemas.user import CreateUser, LoginUser
from app.services.user import create_user, authenticate_user, create_access_token

router = APIRouter()

@router.get("")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users" : users}

@router.post("/register")
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user.email, user.password)
    return new_user

@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = authenticate_user(db=db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail= "Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    at_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(data={"sub": user.email}, expires_delta=at_expires)
    return {"access_token": access_token, "token_type": "bearer"}

