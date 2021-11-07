from enum import Enum
from pydantic import BaseModel


class ContactCreate(BaseModel):
    name: str
    email: str
    instagram: str
    company_id: int
    position_id: int
    command_id: int
    email_type_id: int


class ContactUpdate:
    pass


class ContactDelete:
    pass


