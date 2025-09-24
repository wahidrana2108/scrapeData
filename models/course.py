from sqlalchemy import Column, Integer, String, Text
from models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, default=30)
