import pandas as pd
from pandas import DataFrame
from app.db.database import get_db
from app.modules.songs.models import Song
from app.modules.comments.models import Comment
from app.modules.contacts.models import Contact


class ExcelExporter:
    def __init__(self, path: str, sheet: str):
        self.path = path
        self.sheet = sheet
        self.session = next(get_db())

    @property
    def df(self):
        df: DataFrame = pd.read_excel(self.path, self.sheet, engine="openpyxl")
        return df

    def export_excel(self):
        df = self.df
        df = df.fillna("")

        for row in range(len(df)):
            contact_name = str(df.loc[row, "Name"]).strip()
            contact = self.session.query(Contact).filter_by(name=contact_name).first()
            if not contact:
                continue
            for sent_song in contact.songs:
                try:
                    sent = str(df.loc[row, f"{sent_song.name}"]).strip()
                except KeyError:
                    raise KeyError(
                        f"There is no column named {sent_song.name}, tip: check spelling"
                    )
                if not sent:
                    df.loc[row, f"{sent_song.name}"] = "Sent"

        df.to_excel("Excel/hustle_test.xlsx", "Emails")


if __name__ == "__main__":
    path = r"~/Personal/sampa-back/Excel/HUSTLE(15).xlsx"
    sheet = "Emails"
    exporter = ExcelExporter(path, sheet)
    exporter.export_excel()
