from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import verify_jwt

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()  # للتحقق من Authorization header

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    return payload

# endpoint /me
@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
