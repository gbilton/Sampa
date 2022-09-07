import pandas as pd
from pandas import DataFrame

from app.db.database import get_db
from app.modules.emails.models import EmailAddress


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
            email_address = str(df.loc[row, "Email"]).strip()
            email = self.session.query(EmailAddress).filter_by(address=email_address).first()
            if not email:
                continue
            for sent_song in email.songs:
                try:
                    sent = str(df.loc[row, f"{sent_song.name}"]).strip()
                except KeyError:
                    raise KeyError(
                        f"There is no column named {sent_song.name}, tip: check spelling"
                    )
                if not sent:
                    df.loc[row, f"{sent_song.name}"] = "Sent"

        df.to_excel("Excel/exported_hustle.xlsx", "Emails")


if __name__ == "__main__":
    path = r"~/Personal/sampa-back/Excel/HUSTLE(32).xlsx"
    sheet = "Emails"
    exporter = ExcelExporter(path, sheet)
    exporter.export_excel()
