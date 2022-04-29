from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.db.database import Base


roster_table = Table(
    "roster_rel",
    Base.metadata,
    Column("Roster ID", ForeignKey("rosters.id"), primary_key=True),
    Column("Contact ID", ForeignKey("contacts.id"), primary_key=True),
)


class Roster(Base):
    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    contacts = relationship("Contact", secondary=roster_table, backref="rosters")
