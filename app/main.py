# type: ignore

from fastapi import FastAPI

from . import models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {}


@app.get("/items/")
async def read_item(name: str, link: str):
    session = next(get_db())
    song = models.Song(name=name, link=link)
    session.add(song)
    session.commit()
    return name

 