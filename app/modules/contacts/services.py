from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from app.modules.categories.models import Category
from app.modules.comments.models import Comment
from app.modules.emails.models import Command, EmailType

from app.modules.rosters.models import Roster
from app.modules.companies.models import Company
from app.modules.genres.models import Genre
from app.modules.positions.models import Position
from app.modules.songs.models import Song

from ...models import Contact
from app.db.database import get_db


class ExcelImporter:
    def __init__(self, path: str, sheet: str):
        self.path = path
        self.sheet = sheet
        self.session = next(get_db())

    @property
    def df(self):
        df: DataFrame = pd.read_excel(self.path, self.sheet, engine='openpyxl')
        return df

    def create_roster(self):
        df = self.df
        df = df.fillna('')

        for row in range(len(df)):
            name = str(df.loc[row, "Roster"]).strip()
            if name == '':
                continue
            
            roster_dict = {
                "name": name
            }

            if not self.exists(Roster, roster_dict):
                roster_orm = Roster(**roster_dict)
                self.session.add(roster_orm)
                self.session.commit()

    def create_company(self):
        df = self.df
        df = df.fillna('')
        
        for row in range(len(df)):
            category_id = self.get_object_id(Category, df.loc[row, "Category"])
    
            company_dict = {
                "name": str(df.loc[row, "Company"]).strip(),
                "category_id": category_id
            }

            if company_dict['name'] == '':
                continue

            if not self.exists(Company, company_dict):
                company_orm = Company(**company_dict)
                self.session.add(company_orm)
                self.session.commit()

    def create_contact(self):
        df = self.df
        df = df.fillna('')
        
        for row in range(len(df)):
            company_id = self.get_object_id(
                Company, str(df.loc[row, "Company"]).strip()
            )

            command_id = self.get_object_id(
                Command, str(df.loc[row, "Command"]).strip()
            )

            email_type_id = self.get_object_id(
                EmailType, str(df.loc[row, "Email Type"]).strip()
            )

            position_id = self.get_object_id(
                Position, str(df.loc[row, "Position"]).strip()
            )

            contact_dict = {
                "name": str(df.loc[row, "Name"]).strip(),
                "email": str(df.loc[row, "Email"]).strip(),
                "instagram": str(df.loc[row, "Instagram"]).strip(),
                "location": str(df.loc[row, "Location"]).strip(),
                "email_type_id": email_type_id,
                "command_id": command_id,
                "company_id": company_id,
                "position_id": position_id
            }

            if contact_dict['name'] == '':
                continue
            
            if not self.exists(Contact, contact_dict):
                contact_orm = Contact(**contact_dict)
                self.session.add(contact_orm)
                self.session.commit()             

    def create_comment(self):
        df = self.df
        df = df.fillna('')

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                continue

            comment_text = str(df.loc[row, "Comments"]).strip()

            if comment_text != '':
                comment = Comment(text=comment_text, contact_id=contact.id)
                exists = self.session.query(Comment).filter_by(text=comment_text, contact_id=contact.id).first()
                if not exists:
                    self.session.add(comment)
                    self.session.commit()

    def link_roster(self):
        df = self.df
        df = df.fillna('')

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(
                name=contact_name).first()
            if not contact:
                continue
            roster_name = str(df.loc[row, "Roster"]).strip()
            roster = self.session.query(Roster).filter_by(name=roster_name).first()
            if not roster:
                continue
            if roster not in contact.rosters:
                contact.rosters.append(roster)
                self.session.add(contact)
        self.session.commit()
    
    def link_genre(self):
        df = self.df
        df = df.fillna('')

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(
                name=contact_name).first()
            if not contact:
                continue
            genre_name = str(df.loc[row, "Genre"]).strip()
            genre = self.session.query(Genre).filter_by(name=genre_name).first()
            if not genre:
                continue
            if genre not in contact.genres:
                contact.genres.append(genre)
                self.session.add(contact)
        self.session.commit()

    def create_sent(self, columns: List[str]):
        df = self.df
        df = df.fillna('')

        for song_name in columns:
            for row in range(len(df)):
                sent = df.loc[row, song_name]
                contact_name = str(df.loc[row, 'Name']).strip()

                contact = self.session.query(Contact).filter_by(name=contact_name).first()
                song = self.session.query(Song).filter_by(name=song_name).first()
                
                if not contact:
                    continue

                if sent:
                    if song not in contact.songs:
                        contact.songs.append(song)   
                        self.session.add(contact) 
        self.session.commit()

    def get_object_id(self, Obj, obj_name: str) -> int:
        obj = self.session.query(Obj).filter_by(name=obj_name).first()
        if not obj:
            return None
        return obj.id

    def exists(self, Obj, obj_dict):
        exists = self.session.query(Obj).filter_by(name=obj_dict['name']).first()
        if not exists:
            return False
        return True

    def create_all(self):
        self.create_roster()
        self.create_company()
        self.create_contact()
        self.create_comment()
        self.link_genre()
        self.link_roster()

if __name__ == "__main__":
    path = r"~/Personal/sampa-back/Excel/Hustle.xlsx"
    sheet = 'Emails'
    importer = ExcelImporter(path, sheet)
    importer.create_all()

    songs = [
        'Objectify Me',
        'Keep In Touch',
        'Do You Believe',
        'Skrt Skrt',
        'Live Another Day',
        'Love Me',
        'Sleep Alone'
    ]
    # importer.create_sent(songs)
    