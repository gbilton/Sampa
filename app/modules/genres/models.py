from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from ...database import Base


genres_songs_table = Table('song_genres', Base.metadata,
                     Column('Song ID', ForeignKey(
                         'songs.id'), primary_key=True),
                     Column('Genre ID', ForeignKey(
                         'genres.id'), primary_key=True)
                     )
                     
genres_contacts_table = Table('contacts_genres', Base.metadata,
                     Column('Contact ID', ForeignKey(
                         'contacts.id'), primary_key=True),
                     Column('Genre ID', ForeignKey(
                         'genres.id'), primary_key=True)
                     )
                     
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    
    song_rel = relationship('Song', secondary=genres_songs_table)
    contanct_rel = relationship('Contact', secondary=genres_contacts_table)
