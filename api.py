from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Vacancy(BaseModel):
    name: str
    salary_from: int
    salary_to: int
    website: str
    datetime: str
  
VACANCY_DB = [
  Vacancy(name = "Системный аналитик", salary_from = 150000, salary_to = 200000, website = "ekaterinburg.hh.ru", datetime = "2022-07-12 16:01:06.799687"),
  Vacancy(name = "Аналитик/Бизнес-аналитик", salary_from = 90000, salary_to = 0, website = "ekaterinburg.hh.ru", datetime = "2022-07-12 16:01:06.831690"),
  Vacancy(name = "Аналитик 1С", salary_from = 80000, salary_to = 150000, website = "ekaterinburg.hh.ru", datetime = "2022-07-12 16:01:06.847698"),
  Vacancy(name = "Аналитик отдела продаж", salary_from = 60000, salary_to = 0, website = "ekb.zarplata.ru", datetime = "2022-07-12 16:06:21.894380"),
  Vacancy(name = "Маркетолог-аналитик", salary_from = 50000, salary_to = 75000, website = "ekb.zarplata.ru", datetime = "2022-07-12 16:06:22.014433"),
]


@app.get("/vacancies")
def read_vacancies():
    return VACANCY_DB


@app.get("/vacancy/{item_id}")
def read_vacancy(item_id: int):
    return VACANCY_DB[item_id]

@app.post("/vacancy/create")
def create_vacancy(item: Vacancy):
    VACANCY_DB.append(item)
    return {"status":"ok"}


@app.put("/vacancy/{item_id}")
def update_vacancy(item_id: int, item: Vacancy):
    VACANCY_DB[item_id] = item
    return {"status":"ok"}

@app.delete("/vacancy/{item_id}")
def delete_vacancy(item_id: int):
    del VACANCY_DB[item_id]
    return {"status":"ok"}