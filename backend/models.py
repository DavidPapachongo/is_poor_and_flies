from typing import Collection
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean 

from database import Base


class Music(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    song = Column(String, index=True)
    title = Column(String, default="unknown")
    artist = Column(String, default="unknown")
    album = Column(String, default="unknown")
    year = Column(Integer, nullable=True)
    liked = Column(Boolean, default=False)