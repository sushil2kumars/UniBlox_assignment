from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import app
from app import get_db
from models import User
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY 

router = APIRouter()

# Dependency to get the database session


# Function to create a new JWT token
def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=username)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/signin")
def signin(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create a JWT token for authentication
    token_data = {"sub": str(user.id)}
    token = create_jwt_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

