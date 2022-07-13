from datetime import datetime
from typing import Union

from pydantic import BaseModel

class VacancyBase(BaseModel):
  name: str
  salary_from: int
  salary_to: int = None
  website: str


class VacancyCreate(VacancyBase):
  pass


class Vacancy(VacancyBase):
    datetime: datetime
    id: int

    class Config:
        orm_mode = True