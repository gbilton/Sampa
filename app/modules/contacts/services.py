import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy.orm.session import make_transient

from ...schemas import ContactCreate
from ...models import Contact
from ...main import get_db


class ExcelImporter:
    def __init__(self, path: str, sheet: str):
        self.path = path
        self.sheet = sheet
        self.session = next(get_db())

    @property
    def df(self):
        df: DataFrame = pd.read_excel(self.path, self.sheet, engine='openpyxl')
        return df
    
    def make_dict(self):
        df = self.df
        df = df.apply(lambda x: pd.Series(x.dropna().values))
        print(df.query("Name == '3 Beat Team'"))
        
        for row in range(len(df)):
            contact_dict = {
                "name": str(df.loc[row, "Name"]).strip(),
                "email": str(df.loc[row, "Email"]).strip(),
                "instagram": str(df.loc[row, "Instagram"]).strip(),
                "company": str(df.loc[row, "Company"]).strip(),
                "genre": str(df.loc[row, "Genre"]).strip(),
                "type_": str(df.loc[row, "Type"]).strip(),
                "position": str(df.loc[row, "Position"]).strip(),
                "site": str(df.loc[row, "Site"]).strip()
            }
        

            if not self.exists(contact_dict):
                contact_orm = Contact(**contact_dict)
                self.session.add(contact_orm)
        self.session.commit()
        return contact_dict
    
    def exists(self, contact_dict):
        exists = self.session.query(Contact).filter_by(**contact_dict).first()
        if not exists:
            return False
        return True

        

if __name__ == "__main__":
    path = r"~/Personal/Sampa/Excel/Email Hustle.xlsx"
    sheet = 'Emails'
    importer = ExcelImporter(path, sheet)
    d = importer.make_dict()
    print(d)
    