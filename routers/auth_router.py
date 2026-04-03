from fastapi import APIRouter, HTTPException
from models.user_model import UserRegister, UserLogin
from user_excel import read_users, save_users
from utils.jwt_handler import create_jwt
from passlib.hash import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

# Register
@router.post("/register")
def register(user: UserRegister):
    df = read_users()

    if user.email in df["email"].values:
        raise HTTPException(400, "Email already exists")

    new_id = 1 if df.empty else int(df["id"].max()) + 1

    hashed_password = bcrypt.hash(user.password)

    new_user = {
        "id": new_id,
        "email": user.email,
        "password": hashed_password,
        "role": "customer"
    }

   
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    save_users(df)

    return {"message": "User created"}

# Login
@router.post("/login")
def login(user: UserLogin):
    df = read_users()
    db_user = df[df["email"] == user.email]

    if db_user.empty:
        raise HTTPException(404, "User not found")

    db_user = db_user.iloc[0]

    if not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(400, "Wrong password")

    token = create_jwt({"user_id": db_user["id"], "role": db_user["role"]})
    return {"message": "Login success", "token": token}
