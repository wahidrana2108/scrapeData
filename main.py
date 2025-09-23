from fastapi import FastAPI
from api import routes
from db import engine
from models import base  # Base class
from models import student, course, enrollment, scraped

app = FastAPI()

# all tables create on startup event
@app.on_event("startup")
def on_startup():
    base.Base.metadata.create_all(bind=engine)

# include all routes
app.include_router(routes.router)
