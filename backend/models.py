from typing import Collection
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean 

from database import Base


class Music(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    title = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    album = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    liked = Column(Boolean, default=False)