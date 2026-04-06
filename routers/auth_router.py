from fastapi import APIRouter, HTTPException
from models.user_model import UserRegister, UserLogin
from utils.jwt_handler import create_jwt
from passlib.hash import bcrypt
from database import get_connection  # استخدام DB بدل Excel

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    # التحقق من وجود الايميل مسبقاً
    cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(400, "Email already exists")

    hashed_password = bcrypt.hash(user.password)

    cursor.execute(
        "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
        (user.email, hashed_password, "customer")
    )
    conn.commit()
    conn.close()

    return {"message": "User created"}


@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (user.email,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user:
        raise HTTPException(404, "User not found")

    if not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(400, "Wrong password")

    token = create_jwt({"user_id": db_user["id"], "role": db_user["role"]})
    return {"message": "Login success", "token": token}
