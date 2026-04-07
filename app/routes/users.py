from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import verify_jwt
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")
         
    return user

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

