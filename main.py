from fastapi import FastAPI
from excel import init_users                     
from routers.auth_router import router as auth_router   
from routers.users_router_CRUD import router as users_router  


app = FastAPI(title="E-Commerce API")

app.include_router(auth_router)

init_users()
