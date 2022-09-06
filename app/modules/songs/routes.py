from typing import List

from fastapi import APIRouter, HTTPException

from app.exceptions import NotFound
from app.modules.songs.services import SongService

from .schemas import SongResponse

song_router = APIRouter()
song_service = SongService()


@song_router.post("/songs/", response_model=SongResponse)
async def add_song(name: str, link: str):
    try:
        return song_service.add_song(link, name)
    except NotFound as error:
        raise HTTPException(404, detail=str(error))


@song_router.post("/songs/genre", response_model=SongResponse)
async def add_genres(song_name: str, genres: List[str]):
    try:
        return song_service.add_genres(song_name, genres)
    except NotFound as error:
        raise HTTPException(404, detail=str(error))
