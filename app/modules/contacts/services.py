import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy.orm.session import make_transient
from app.modules.categories.models import Category

from app.modules.companies.models import Company
from app.modules.genres.models import Genre
from app.modules.positions.models import Position

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
    
    def create_company(self):
        df = self.df
        df = df.fillna('')
        
        for row in range(len(df)):
            category_id = self.get_object_id(Category, df.loc[row, "Type"])
    
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
                Company, str(df.loc[row, "Company"]))

            genre_id = self.get_object_id(
                Genre, str(df.loc[row, "Genre"]))

            position_id = self.get_object_id(
                Position, str(df.loc[row, "Position"]))

            if not company_id and genre_id and position_id:
                print('Failed')
                continue

            contact_dict = {
                "name": str(df.loc[row, "Name"]).strip(),
                "email": str(df.loc[row, "Email"]).strip(),
                "instagram": str(df.loc[row, "Instagram"]).strip(),
                "company_id": company_id,
                "genre_id": genre_id,
                "position_id": position_id
            }

            if contact_dict['name'] == '':
                continue
            
            if not self.exists(Contact, contact_dict):
                contact_orm = Contact(**contact_dict)
                self.session.add(contact_orm)
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
        self.create_company()
        self.create_contact()

        

if __name__ == "__main__":
    path = r"~/Personal/Sampa/Excel/Email Hustle.xlsx"
    sheet = 'Emails'
    importer = ExcelImporter(path, sheet)
    importer.create_all()
   
    