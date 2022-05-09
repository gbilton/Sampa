import os
from typing import List
import pandas as pd
from pandas.core.frame import DataFrame
from app.modules.categories.models import Category
from app.modules.comments.models import Comment
from app.modules.emails.models import Command, EmailAddress, EmailType
from app.modules.emails.schemas import EmailAddressCreate

from app.modules.rosters.models import Roster
from app.modules.companies.models import Company
from app.modules.genres.models import Genre
from app.modules.songs.models import Song
from app.modules.emails.models import EmailAddress

from .models import Contact
from app.db.database import get_db


class ExcelImporter:
    def __init__(self, path: str, sheet: str):
        self.path = path
        self.sheet = sheet
        self.session = next(get_db())

    @property
    def df(self):
        df: DataFrame = pd.read_excel(self.path, self.sheet, engine="openpyxl")
        return df

    def _unpack_many(self, content: List[str]):
        final_content = []
        for i in content:
            if "-" in i:
                x = i.split("-")
                for j in x:
                    final_content.append(j.strip())
            else:
                final_content.append(i.strip())
        return final_content

    def _create_roster(self):
        df = self.df
        df = df.fillna("")
        roster_df = df["Roster"][df["Roster"].notnull()]
        sorted_rosters = sorted(list(set(self._unpack_many(roster_df))))
        sorted_rosters = [name for name in sorted_rosters if name != ""]
        self.session.add_all([Roster(name=name) for name in sorted_rosters])
        self.session.commit()

    def _create_company(self):
        df = self.df
        df = df.fillna("")

        companies = []
        for row in range(len(df)):
            category_id = self._get_object_id(Category, df.loc[row, "Category"])

            company_dict = {
                "name": str(df.loc[row, "Company"]).strip(),
                "category_id": category_id,
            }

            if company_dict["name"] == "":
                continue

            if company_dict["name"] not in [company["name"] for company in companies]:
                companies.append(company_dict)

        self.session.add_all([Company(**company_dict) for company_dict in companies])
        self.session.commit()

    def _create_contact(self):
        df = self.df
        df = df.fillna("")

        contacts = []
        for row in range(len(df)):
            company_id = self._get_object_id(
                Company, str(df.loc[row, "Company"]).strip()
            )

            if not company_id:
                raise Exception(f"Contact in row {row + 2} Company not in db.")

            contact_dict = {
                "name": str(df.loc[row, "Name"]).strip(),
                "company_id": company_id,
            }

            if contact_dict["name"] == "":
                continue

            if contact_dict["name"] not in [contact["name"] for contact in contacts]:
                contacts.append(contact_dict)

        self.session.add_all([Contact(**contact_dict) for contact_dict in contacts])
        self.session.commit()

    def _create_email_addresses(self):
        df = self.df
        df = df.fillna("")

        emails = []
        for row in range(len(df)):
            contact_id = self._get_object_id(Contact, str(df.loc[row, "Name"]).strip())

            if not contact_id:
                raise Exception(
                    f"Email address without specified contact on row {row+2}"
                )

            command_id = self._get_object_id(
                Command, str(df.loc[row, "Command"]).strip()
            )
            if not command_id:
                raise Exception(f"Contact in row {row + 2} Command not in db.")

            email_type_id = self._get_object_id(
                EmailType, str(df.loc[row, "Email Type"]).strip()
            )
            if not email_type_id:
                raise Exception(f"Contact in row {row + 2} Email Type not in db.")

            email_address = EmailAddressCreate(
                contact_id=contact_id,
                address=str(df.loc[row, "Email"]).strip(),
                email_type_id=email_type_id,
                command_id=command_id,
            )

            if email_address.address == "":
                raise Exception("Empty email address")

            if email_address.address not in [email.address for email in emails]:
                emails.append(email_address)

        self.session.add_all([EmailAddress(**email.dict()) for email in emails])
        self.session.commit()

    def _create_comment(self):
        df = self.df
        df = df.fillna("")

        comments = []
        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                raise Exception(f"Contact {contact_name} not found in db.")

            comment_text = str(df.loc[row, "Comments"]).strip()

            if comment_text != "":
                comment = Comment(text=comment_text, contact_id=contact.id)
                comments.append(comment)
        unique_comments = list(set(comments))
        self.session.add_all(unique_comments)
        self.session.commit()

    def _link_contact_roster(self):
        df = self.df
        df = df.fillna("")

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                raise Exception(f"Contact {contact_name} not found in db.")
            roster_name = str(df.loc[row, "Roster"]).strip()
            if roster_name == "":
                continue

            if "-" in roster_name:
                roster_names = roster_name.split("-")
                roster_names = [roster_name.strip() for roster_name in roster_names]
            else:
                roster_names = [roster_name]

            for roster_name in roster_names:
                roster = self.session.query(Roster).filter_by(name=roster_name).first()
                if not roster:
                    raise Exception(
                        f"Roster {roster_name} not found in db. Row {row+2}"
                    )
                if roster not in contact.rosters:
                    contact.rosters.append(roster)
                    self.session.add(contact)
        self.session.commit()

    def _link_contact_genre(self):
        df = self.df
        df = df.fillna("")

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                raise Exception(f"Contact {contact_name} not found in db.")
            genre_name = str(df.loc[row, "Genre"]).strip()

            if genre_name == "":
                continue
            if "-" in genre_name:
                genres_names = genre_name.split("-")
                genre_names = [genre.strip() for genre in genres_names]
            else:
                genre_names = [genre_name]

            for genre_name in genre_names:
                genre = self.session.query(Genre).filter_by(name=genre_name).first()
                if not genre:
                    raise Exception(f"Genre {genre_name} not found in db. row {row+2}")
                if genre not in contact.genres:
                    contact.genres.append(genre)
                    self.session.add(contact)
        self.session.commit()

    def _link_song_genre(self):
        df = self.df[["Songs", "Song Genres"]]
        df = df.fillna("")
        for row in range(len(df)):
            song_name = str(df.loc[row, "Songs"]).strip()
            if not song_name:
                continue
            song = self.session.query(Song).filter_by(name=song_name).first()
            if not song:
                raise Exception(f"Song {song_name} not found in db.")
            genre_name = str(df.loc[row, "Song Genres"]).strip()
            if not genre_name:
                continue
            if genre_name == "All Genres":
                raise Exception("Songs cannot have genre type All Genres.")
            if "-" in genre_name:
                genres_names = genre_name.split("-")
                genre_names = [genre.strip() for genre in genres_names]
            else:
                genre_names = [genre_name]

            for genre_name in genre_names:
                genre = self.session.query(Genre).filter_by(name=genre_name).first()
                if not genre:
                    raise Exception(f"genre {genre} not found in database. row {row+3}")
                if genre not in song.genres:
                    song.genres.append(genre)
                    self.session.add(song)
        self.session.commit()

    def _link_sent_songs(self):
        df = self.df
        df = df.fillna("")

        songs = self.session.query(Song).all()
        for row in range(len(df)):
            email_address = str(df.loc[row, "Email"]).strip()
            email = (
                self.session.query(EmailAddress)
                .filter_by(address=email_address)
                .first()
            )
            if not email:
                raise Exception(f"Email {email_address} not found in db.")
            for song in songs:
                try:
                    sent = str(df.loc[row, f"{song.name}"]).strip()
                except KeyError:
                    raise KeyError(
                        f"There is no column named {song.name}, tip: check spelling"
                    )
                if sent:
                    if song not in email.songs:
                        email.songs.append(song)
                        self.session.add(email)
        self.session.commit()

    def _create_songs(self):
        df = self.df[["Songs", "Links"]]
        df = df.fillna("")

        songs = []
        for row in range(len(df)):
            song_name = str(df.loc[row, "Songs"]).strip()
            song_link = str(df.loc[row, "Links"]).strip()

            if song_name == "":
                continue

            song_dict = {"name": song_name, "link": song_link}

            if song_dict["name"] not in [song["name"] for song in songs]:
                songs.append(song_dict)

        self.session.add_all([Song(**song_dict) for song_dict in songs])
        self.session.commit()

    def _create_sent(self, columns: List[str]):
        df = self.df
        df = df.fillna("")

        for song_name in columns:
            for row in range(len(df)):
                sent = df.loc[row, song_name]
                email_address = str(df.loc[row, "Email"]).strip()

                email = (
                    self.session.query(EmailAddress)
                    .filter_by(name=email_address)
                    .first()
                )
                song = self.session.query(Song).filter_by(name=song_name).first()

                if not email:
                    raise Exception(f"Contact {email_address} not found in db.")

                if sent:
                    if song not in email.songs:
                        email.songs.append(song)
                        self.session.add(email)
        self.session.commit()

    def _get_object_id(self, Obj, obj_name: str) -> int:
        obj = self.session.query(Obj).filter_by(name=obj_name).first()
        if not obj:
            return None
        return obj.id

    def _exists(self, Obj, obj_dict):
        exists = self.session.query(Obj).filter_by(name=obj_dict["name"]).first()
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
            raise Exception("File type not .xlsx")

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
            "Song Genres",
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
        ]
        missing_rows = [
            i + 2
            for i in self.df[self.df[essential_columns].isnull().any(axis=1)].index
        ]
        if missing_rows:
            raise Exception(f"Missing values in rows {missing_rows}")

    def create_all(self):
        self._verify_excel()
        self._create_roster()
        self._create_company()
        self._create_contact()
        self._create_email_addresses()
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

    engine.execute(
        "TRUNCATE categories, commands, comments, companies, contacts, contacts_genres, email_types, genres, roster_rel, rosters, sent, song_genres, songs CASCADE;"
    )

    initializer = Initializer()
    initializer.add_bulk_data(data)

    path = r"~/Personal/sampa-back/Excel/HUSTLE(26).xlsx"
    sheet = "Emails"
    importer = ExcelImporter(path, sheet)
    importer.create_all()
