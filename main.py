from fastapi import FastAPI
from routers import auth, users
from database import init_db

app = FastAPI(title="User Auth API with DB")


init_db()

# تسجيل الـ routers
app.include_router(auth.router)
app.include_router(users.router)
