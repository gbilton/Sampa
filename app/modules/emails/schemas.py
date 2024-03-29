from pydantic import BaseModel


class EmailAddressCreate(BaseModel):
    address: str
    contact_id: int
    command_id: int
    email_type_id: int
