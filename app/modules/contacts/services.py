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
        for row in range(len(df)):
            contact_dict = {
                "name": df.loc[row, "Name"],
                "email": df.loc[row, "Email"],
                "instagram": df.loc[row, "Instagram"],
                "company": df.loc[row, "Company"],
                "genre": df.loc[row, "Genre"],
                "type_": df.loc[row, "Type"],
                "position": df.loc[row, "Position"],
                "site": df.loc[row, "Site"]
            }
        
            contact_orm = Contact(**contact_dict)
            self.session.add(contact_orm)
        self.session.commit()
        return contact_dict
    


        

if __name__ == "__main__":
    path = r"~/Personal/Sampa/Excel/Email Hustle.xlsx"
    sheet = 'Emails'
    importer = ExcelImporter(path, sheet)
    d = importer.make_dict()
    print(d)
    