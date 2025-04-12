from fastapi import FastAPI

from app.models.user import Base
from app.database.db import engine
from app.api.routes import user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, prefix="/users")

