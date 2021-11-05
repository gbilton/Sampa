from .main import get_db
from .modules.categories.models import Category
from .modules.genres.models import Genre
from .modules.positions.models import Position


def initial_data():
    categories = [
        "Publisher",
        "Label",
        "Management",
        "Full service",
        "Artist"
    ]
    genres = [
        "Hip Hop",
        "Country",
        "All Genres",
        "Pop",
        "EDM"
    ]
    positions = [
        "A&R",
        "Manager",
        "Other",
        "General"
    ]
    
    session = next(get_db()) 

    for i in categories:
        category = Category(name=i)
        session.add(category)
    for i in genres:
        genre = Genre(name=i)
        session.add(genre)
    for i in positions:
        position = Position(name=i)
        session.add(position)
    
    session.commit()
    


initial_data()