from fastapi import FastAPI

from api.auth import auth_api, db_api
from api.routers import attendance_records, done, task

app = FastAPI()

app.include_router(task.router)
app.include_router(done.router)
app.include_router(db_api.router)
app.include_router(auth_api.router)
app.include_router(attendance_records.router)
