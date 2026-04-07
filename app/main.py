from fastapi import FastAPI
from database import Base, engine
import models.category
import models.product
import models.user
from routes import categories, product, auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Final E-Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 إنشاء الجداول في الداتابيز
Base.metadata.create_all(bind=engine)

# 📌 ربط الـ routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(product.router)