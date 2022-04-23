import os
from plistlib import InvalidFileException
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

from .models import Contact
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

    def _unpack_many(self, content: List[str]):
        final_content = []
        for i in content:
            if "-" in i:
                x = i.split('-')
                for j in x:
                    final_content.append(j.strip())
            else:
                final_content.append(i.strip())
        return final_content

    def _create_roster(self):
        df = self.df
        df = df.fillna('')
        roster_df = df["Roster"][df["Roster"].notnull()]
        sorted_rosters = sorted(list(set(self._unpack_many(roster_df))))
        sorted_rosters = [name for name in sorted_rosters if name != '']
        self.session.add_all([Roster(name=name) for name in sorted_rosters])
        self.session.commit()

    def _create_company(self):
        df = self.df
        df = df.fillna('')
        
        companies = []
        for row in range(len(df)):
            category_id = self._get_object_id(Category, df.loc[row, "Category"])
    
            company_dict = {
                "name": str(df.loc[row, "Company"]).strip(),
                "category_id": category_id
            }

            if company_dict['name'] == '':
                continue

            if company_dict["name"] not in [company["name"] for company in companies]:
                companies.append(company_dict)

        self.session.add_all([Company(**company_dict) for company_dict in companies])
        self.session.commit()

    def _create_contact(self):
        df = self.df
        df = df.fillna('')

        contacts = []
        for row in range(len(df)):
            company_id = self._get_object_id(
                Company, str(df.loc[row, "Company"]).strip()
            )

            command_id = self._get_object_id(
                Command, str(df.loc[row, "Command"]).strip()
            )

            email_type_id = self._get_object_id(
                EmailType, str(df.loc[row, "Email Type"]).strip()
            )

            # position_id = self._get_object_id(
            #     Position, str(df.loc[row, "Position"]).strip()
            # )

            contact_dict = {
                "name": str(df.loc[row, "Name"]).strip(),
                "email": str(df.loc[row, "Email"]).strip(),
                # "instagram": str(df.loc[row, "Instagram"]).strip(),
                # "location": str(df.loc[row, "Location"]).strip(),
                "email_type_id": email_type_id,
                "command_id": command_id,
                "company_id": company_id,
                # "position_id": position_id
            }

            if contact_dict['name'] == '':
                continue
            
            if contact_dict["name"] not in [contact["name"] for contact in contacts]:
                contacts.append(contact_dict)

        self.session.add_all([Contact(**contact_dict)
                             for contact_dict in contacts])
        self.session.commit()

    def _create_comment(self):
        df = self.df
        df = df.fillna('')

        comments = []
        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                continue

            comment_text = str(df.loc[row, "Comments"]).strip()

            if comment_text != '':
                comment = Comment(text=comment_text, contact_id=contact.id)
                comments.append(comment)
        unique_comments = list(set(comments))
        self.session.add_all(unique_comments)
        self.session.commit()

    def _link_contact_roster(self):
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
    
    def _link_contact_genre(self):
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

    def _link_song_genre(self):
        df = self.df[["Songs", "Song Genres"]]
        df = df.fillna('')
        for row in range(len(df)):
            song_name = str(df.loc[row, "Songs"]).strip()
            song = self.session.query(Song).filter_by(
                name=song_name).first()
            if not song:
                continue
            genre_name = str(df.loc[row, "Song Genres"]).strip()
            genre = self.session.query(Genre).filter_by(
                name=genre_name).first()
            if not genre:
                continue
            if genre not in song.genres:
                song.genres.append(genre)
                self.session.add(song)
        self.session.commit()

    def _link_sent_songs(self):
        df = self.df
        df = df.fillna('')

        songs = self.session.query(Song).all()
        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(
                name=contact_name).first()
            if not contact:
                continue
            for song in songs:
                try:
                    sent = str(df.loc[row, f"{song.name}"]).strip()
                except KeyError:
                    raise KeyError(f"There is no column named {song.name}, tip: check spelling")
                if sent:
                    if song not in contact.songs:
                        contact.songs.append(song)
                        self.session.add(contact)
        self.session.commit()
    
    def _create_songs(self):
        df = self.df[["Songs", "Links"]]
        df = df.fillna('')

        songs = []
        for row in range(len(df)):
            song_name = str(df.loc[row, "Songs"]).strip()
            song_link = str(df.loc[row, "Links"]).strip()

            if song_name == '':
                continue
            
            song_dict = {
                "name": song_name,
                "link": song_link
            }

            if song_dict["name"] not in [song["name"] for song in songs]:
                    songs.append(song_dict)

        self.session.add_all([Song(**song_dict)
                             for song_dict in songs])
        self.session.commit()
    
    def _create_sent(self, columns: List[str]):
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

    def _get_object_id(self, Obj, obj_name: str) -> int:
        obj = self.session.query(Obj).filter_by(name=obj_name).first()
        if not obj:
            return None
        return obj.id

    def _exists(self, Obj, obj_dict):
        exists = self.session.query(Obj).filter_by(name=obj_dict['name']).first()
        if not exists:
            return False
        return True

    def _verify_excel(self):
        self._verify_extension()
        self._verify_columns()
        self._verify_rows()
    
    def _verify_extension(self):
        _, file_extension = os.path.splitext(self.path)
        if file_extension != ".xlsx":
            raise InvalidFileException("File type not .xlsx")

    def _verify_columns(self):
        expected_columns = [
            "Company",
            "Name",
            "Email",
            "Command",
            "Comments",
            "Site",
            "Email Type",
            "Genre",
            "Category",
            "Roster",
            "Songs",
            "Links",
            "Song Genres"
        ]

        for column in expected_columns:
            if column not in self.df.columns:
                raise Exception(f"Excel file missing column {column}.")

    def _verify_rows(self):
        """Checks for null values in collumns that must contain info."""

        essential_columns = [
            "Company",
            "Name",
            "Email",
            "Command",
            "Email Type",
            "Genre",
            "Category"
        ]
        missing_rows = [i+2 for i in self.df[self.df[essential_columns].isnull().any(axis=1)].index]
        if missing_rows:
            raise Exception(f"Missing values in rows {missing_rows}")

    def create_all(self):
        # self._verify_excel()
        self._create_roster()
        self._create_company()
        self._create_contact()
        self._create_comment()
        self._create_songs()
        self._link_contact_genre()
        self._link_contact_roster()
        self._link_song_genre()
        self._link_sent_songs()
        self.session.commit()

if __name__ == "__main__":
    from app.init import Initializer, data
    from .db.database import engine
    
    engine.execute("TRUNCATE categories, commands, comments, companies, contacts, contacts_genres, email_types, genres, positions, roster_rel, rosters, sent, song_genres, songs CASCADE;")

    initializer = Initializer()
    initializer.add_bulk_data(data)

    path = r"~/Personal/sampa-back/Excel/Hustle(1).xlsx"
    sheet = 'Emails'
    importer = ExcelImporter(path, sheet)
    importer.create_all()

    # songs = [
    #     'Objectify Me',
    #     'Keep In Touch',
    #     'Do You Believe',
    #     'Skrt Skrt',
    #     'Live Another Day',
    #     'Love Me',
    #     'Sleep Alone'
    # ]
    # importer.create_sent(songs)