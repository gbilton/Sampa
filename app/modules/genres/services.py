from app.db.database import get_db
from app.modules.genres.models import Genre


class GenreService:
    def add_genre(self, name: str):
        session = next(get_db())
        
        exists = session.query(Genre).filter_by(name=name).first()
        if exists:
            raise "Already in Database..."

        genre = Genre(name=name)
        session.add(genre)
        session.commit()