from enum import Enum

from pydantic import BaseModel


class SongResponse(BaseModel):
    name: str
    link: str

    class Config:
        orm_mode = True


class SongGenreEnum(str, Enum):
    edm = "EDM"
    all_genre = "All Genres"
