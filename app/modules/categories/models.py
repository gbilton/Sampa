from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relation, relationship

from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    companies = relationship('Company')
