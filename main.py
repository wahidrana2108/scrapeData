from fastapi import FastAPI
from db import engine
from api import routes
# main.py

from models.base import Base



Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(routes.router)
