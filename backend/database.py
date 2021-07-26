import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URl = os.environ["SQLALCHEMY_DATABASE_URl"]

engine = create_engine(SQLALCHEMY_DATABASE_URl)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
