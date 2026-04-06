from fastapi import APIRouter, HTTPException
from models.user_model import UserRegister
from passlib.hash import bcrypt
from database import get_connection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    
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
