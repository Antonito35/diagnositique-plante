from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from services.auth_service import hash_password, verify_password, create_access_token, decode_access_token
from schemas.auth import UserRegisterRequest, UserLoginRequest, AuthTokenResponse, UserOut

router = APIRouter()


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = authorization[7:]
    payload = decode_access_token(token)
    
    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


@router.post("/register", response_model=AuthTokenResponse)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        name=req.name,
        email=req.email,
        hashed_password=hash_password(req.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"user_id": user.id})
    return {
        "access_token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }


@router.post("/login", response_model=AuthTokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user.id})
    return {
        "access_token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
