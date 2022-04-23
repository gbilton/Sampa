from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.db.database import Base
from app.models import Song
from app.models import Comment

sent_table = Table('sent', Base.metadata,
                          Column('Contact ID', ForeignKey(
                              'contacts.id'), primary_key=True),
                          Column('Song ID', ForeignKey(
                              'songs.id'), primary_key=True)
                          )
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String)
    instagram = Column(String)
    location = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    command_id = Column(Integer, ForeignKey('commands.id'))
    email_type_id = Column(Integer, ForeignKey('email_types.id'))

    songs = relationship('Song', secondary=sent_table, backref='contacts')
    comments = relationship('Comment')