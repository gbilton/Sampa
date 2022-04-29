from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.db.database import Base


class EmailType(Base):
    __tablename__ = "email_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    contacts = relationship("Contact", backref="email_types")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    contacts = relationship("Contact", backref="command")


class EmailAdress(Base):
    __tablename__ = "email_addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
