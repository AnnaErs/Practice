from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from . import models, schemas


def get_vacancy(db: Session, vacancy_id: int):
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()


def get_vacancy_by_name(db: Session, name: str):
    return db.query(models.Vacancy).filter(models.Vacancy.name == name).order_by(models.Vacancy.datetime.desc()).first()


def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacancy).offset(skip).limit(limit).all()


def create_vacancy(db: Session, vacancy: schemas.VacancyCreate):
    dt = datetime.now()
    db_vacancy = models.Vacancy(
      name=vacancy.name,
      salary_from = vacancy.salary_from,
      salary_to = vacancy.salary_to,
      website = vacancy.website,
      datetime=dt
      )
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def delete_vacancy(db: Session, vacancy_id: int):
    item = db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).delete()
    db.commit()
    return

def update_vacancy(db: Session, vacancy_id: int, vacancy: schemas.VacancyCreate):
    item = db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()
    item.name=vacancy.name
    item.salary_from = vacancy.salary_from
    item.salary_to = vacancy.salary_to
    item.website = vacancy.website
    db.add(item)
    db.commit()
    db.refresh(item)
    return item