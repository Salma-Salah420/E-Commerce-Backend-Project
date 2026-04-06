from fastapi import APIRouter, HTTPException
from models.user_model import UserLogin
from passlib.hash import bcrypt
from utils.jwt_handler import create_jwt
from database import get_connection

router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    # جلب المستخدم من DB حسب الايميل
    cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user:
        raise HTTPException(404, "User not found")

    # التحقق من كلمة السر المشفرة
    if not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(400, "Wrong password")

    # إنشاء توكن JWT
    token = create_jwt({"user_id": db_user["id"], "role": db_user["role"]})
    return {"message": "Login success", "token": token}
