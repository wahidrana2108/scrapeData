from sqlalchemy import Column, Integer, String, Float
from models.base import Base

class ScrapedResource(Base):
    __tablename__ = "scraped_resources"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    category = Column(String)
    price = Column(Float)
