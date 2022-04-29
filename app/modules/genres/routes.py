from typing import List
from fastapi import APIRouter
from fastapi import HTTPException

from app.exceptions import NotFound
from app.modules.genres.services import GenreService


genre_router = APIRouter()
genre_service = GenreService()


@genre_router.post("/genres")
async def add_song(name: str):
    try:
        genre_service.add_genre(name)
    except:
        print("Something went wrong...")
