from sqlalchemy import Column
from models.person import Person


class Student(Person):
    __tablename__ = "students"
