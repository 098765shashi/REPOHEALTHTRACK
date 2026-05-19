import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User

SECRET = os.getenv("JWT_SECRET", "dev-secret")
ALGO = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def hash_pw(p): return pwd.hash(p)
def verify_pw(p, h): return pwd.verify(p, h)

def make_token(sub: str):
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    if not token: return None
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return db.query(User).filter(User.email == data["sub"]).first()
    except JWTError:
        return None
