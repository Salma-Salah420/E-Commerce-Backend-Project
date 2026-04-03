@router.post("/login")
def login(user: UserLogin):

    df = read_users()

    db_user = df[df["email"] == user.email]

    if db_user.empty:
        raise HTTPException(404, "User not found")

    db_user = db_user.iloc[0]

    if db_user["password"] != user.password:
        raise HTTPException(400, "Wrong password")

    return {"message": "Login success"}
