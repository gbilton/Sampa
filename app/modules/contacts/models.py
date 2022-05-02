from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.db.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    comments = relationship("Comment")
    emails = relationship("EmailAddress", backref="contact")
