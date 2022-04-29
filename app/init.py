from re import S
from typing import Any, List, Tuple
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

    def add_bulk_data(self, data: Tuple[Any, List[str]]):
        for i in data:
            self.add_data(i[0], i[1])


categories = (Category, ["Publisher", "Label", "Management", "Full Service", "Artist"])
genres = (Genre, ["Hip Hop", "Country", "All Genres", "Pop", "EDM", "Alt Pop"])
commands = (
    Command,
    ["Not Emailing", "VIP", "Emailing", "Email not working", "Spam", "Demo Drop"],
)
email_types = (
    EmailType,
    ["Normal Email", "Management Email", "General Email", "RAMPAK Email"],
)

data = [categories, genres, commands, email_types]


if __name__ == "__main__":
    initializer = Initializer()
    for i in data:
        initializer.add_data(i[0], i[1])
