from sqlalchemy import Column, Integer, String
from models.base import Base

class Person(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
