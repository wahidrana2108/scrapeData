from pydantic import BaseModel
from typing import Optional

class ScrapedResourceBase(BaseModel):
    title: str
    url: str
    category: Optional[str] = None
    price: Optional[str] = None
