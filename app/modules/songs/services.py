from typing import List
from app.exceptions import NotFound
from app.db.database import get_db
from app.modules.songs.schemas import SongResponse
from .models import Song
from ..genres.models import Genre


class SongService:
    def add_song(self, link: str, name: str) -> SongResponse:
        session = next(get_db())

        song = Song(name=name, link=link)

        exists = session.query(Song).filter_by(name=name).first()

        if not exists:
            session.add(song)
            session.commit()

        response = SongResponse.from_orm(song)
        return response

    def add_genres(self, song_name: str, genres: List[str]) -> SongResponse:
        session = next(get_db())

        song = session.query(Song).filter_by(name=song_name).first()
        if not song:
            raise NotFound(f"Song '{song_name}' not found!")

        for genre in genres:
            genre_obj = session.query(Genre).filter_by(name=genre).first()
            if not genre_obj:
                raise NotFound(f"Genre '{genre}' not found!")

            song.genres.append(genre_obj)

        session.add(song)
        session.commit()

        response = SongResponse.from_orm(song)
        return response
