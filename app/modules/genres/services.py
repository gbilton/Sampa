from app.db.database import get_db
from app.modules.genres.models import Genre


class GenreService:
    def add_genre(self, name: str):
        session = next(get_db())

        exists = session.query(Genre).filter_by(name=name).first()
        if exists:
            raise Exception("Already in Database...")

        genre = Genre(name=name)
        session.add(genre)
        session.commit()

    @classmethod
    def get_genre(cls, name):
        session = next(get_db())
        genre = session.query(Genre).filter_by(name=name).first()
        if not genre:
            raise ("No genre found!")
        return genre
