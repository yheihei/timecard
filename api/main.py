from fastapi import FastAPI

from api.auth import auth_api, db_api
from api.routers import clock_in

app = FastAPI()

app.include_router(db_api.router)
app.include_router(auth_api.router)
app.include_router(clock_in.router)
