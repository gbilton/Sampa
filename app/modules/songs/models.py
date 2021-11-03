from sqlalchemy import Column, Integer, String

from ...database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)
    
