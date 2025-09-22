from sqlalchemy import Column
from models.person import Person

class Teacher(Person):
    __tablename__ = "teachers"
