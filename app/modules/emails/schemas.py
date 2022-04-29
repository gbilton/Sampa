from pydantic import BaseModel


class EmailAddressCreate(BaseModel):
    address: str
    contact_id: int
