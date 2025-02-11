from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.hashing import hash_password

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email Already Registerd")
    
    if db_username:
        raise HTTPException(status_code=400, detail="try a different username")
    
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, email = user.email, hashed_password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

