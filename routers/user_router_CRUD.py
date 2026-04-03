from fastapi import APIRouter, Depends, HTTPException
from utils.jwt_handler import verify_jwt

router = APIRouter(prefix="/users", tags=["Users"])

def get_current_user(token: str):
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    return payload

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
