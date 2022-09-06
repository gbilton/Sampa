# type: ignore

from fastapi import FastAPI

from . import models, routes, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.song_router)
app.include_router(routes.genre_router)
