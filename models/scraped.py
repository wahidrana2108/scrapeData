from sqlalchemy import Column, Integer, String
from models.base import Base

class ScrapedResource(Base):
    __tablename__ = "scraped_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(String, nullable=True)  # keep as string to avoid parsing issues
