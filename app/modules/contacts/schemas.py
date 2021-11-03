from typing import List, Optional
from pydantic import BaseModel



class ContactCreate(BaseModel):
    name: str
    email: str
    instagram: str
    company: str
    genre: str
    type_: str
    position: str
    site: str 


class ContactUpdate:
    pass


class ContactDelete:
    pass

