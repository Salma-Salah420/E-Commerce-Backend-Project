@router.post("/register")
def register(user: UserRegister):

    df = read_users()

    if user.email in df["email"].values:
        raise HTTPException(400, "Email already exists")

    new_id = 1 if df.empty else int(df["id"].max()) + 1

    new_user = {
        "id": new_id,
        "email": user.email,
        "password": user.password,  # هنشفرها بعد كده
        "role": "customer"
    }

    df = df._append(new_user, ignore_index=True)
    save_users(df)

    return {"message": "User created"}
