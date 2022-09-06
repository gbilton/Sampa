# noqa
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.db.database import Base
from app.modules.comments.models import Comment  # noqa: F401
from app.modules.contacts.models import Contact  # noqa: F401
from app.modules.songs.models import Song  # noqa: F401

sent_table = Table(
    "sent",
    Base.metadata,
    Column("Email Address ID", ForeignKey("email_addresses.id"), primary_key=True),
    Column("Song ID", ForeignKey("songs.id"), primary_key=True),
)


class EmailType(Base):
    __tablename__ = "email_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    emails = relationship("EmailAddress", backref="email_types")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    emails = relationship("EmailAddress", backref="command")


class EmailAddress(Base):
    __tablename__ = "email_addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    command_id = Column(Integer, ForeignKey("commands.id"))
    email_type_id = Column(Integer, ForeignKey("email_types.id"))

    songs = relationship("Song", secondary=sent_table, backref="emails")
