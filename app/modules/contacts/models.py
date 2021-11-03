# type: ignore

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ...database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    instagram = Column(String)
    company = Column(String)
    genre = Column(String)
    type_ = Column(String)
    position = Column(String)
    site = Column(String)



