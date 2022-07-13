from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric,DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary_from = Column(Numeric(10, 2))
    salary_to = Column(Numeric(10, 2))
    website = Column(String)
    datetime = Column(DateTime)

    def __repr__(self):
        return f"{self.name} | {self.salary_from} | {self.salary_to} | {self.website}"
