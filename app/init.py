from re import S
from .db.database import get_db
from .models import *


class Initializer:

    def __init__(self):
        self.session = next(get_db())

    def exists(self, Obj, obj_name):
        exists = self.session.query(Obj).filter_by(name=obj_name).first()
        if exists:
            return True
        return False
        
    def add_data(self, Obj, data):
        for name in data:
            if not self.exists(Obj, name):
                obj = Obj(name=name)
                self.session.add(obj)
                self.session.commit()
    
if __name__ == "__main__":
    categories = (Category, [
        "Publisher",
        "Label",
        "Management",
        "Full service",
        "Artist"
    ])
    genres = (Genre,[
        "Hip Hop",
        "Country",
        "All Genres",
        "Pop",
        "EDM",
        "Alt Pop"
    ])
    positions = (Position,[
        "A&R",
        "Manager",
        "Other",
        "General"
    ])
    commands = (Command,[
        "Not Emailing",
        "VIP",
        "Emailing"
    ])
    email_types = (EmailType,[
        "Normal Email",
        "Management Email",
        "General Email"
    ])

    data = [categories, genres, positions, commands, email_types]

    initializer = Initializer()

    for i in data:
        initializer.add_data(i[0], i[1])
