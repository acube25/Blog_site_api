from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_db
from app.models.user import User
from app.utils.hashing import verify_password
from app.core.security import create_access_token
from datetime import timedelta
from app.core.security import verify_token

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["user_id"]

@router.post("/login")
def login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == from_data.username).first()
    if not user or not verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"user_id": user.id}, expire_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}