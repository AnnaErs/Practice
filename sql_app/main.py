from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/vacancies/", response_model=schemas.Vacancy)
def create_vacancy(vacancy: schemas.VacancyCreate, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy_by_name(db, name=vacancy.name)
    if db_vacancy and db_vacancy.salary_from == vacancy.salary_from:
        raise HTTPException(status_code=400, detail="Vacancy already exist")
    return crud.create_vacancy(db=db, vacancy=vacancy)


@app.get("/vacancies/", response_model=List[schemas.Vacancy])
def read_vacancies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vacancies = crud.get_vacancies(db, skip=skip, limit=limit)
    return vacancies


@app.get("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def read_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy

@app.delete("/vacancies/{vacancy_id}", response_model=dict)
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    crud.delete_vacancy(db, vacancy_id)
    return {
        "status":"ok"
    }

@app.put("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def update_vacancy(vacancy_id: int, vacancy: schemas.VacancyCreate , db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    
    return crud.update_vacancy(db, vacancy_id, vacancy)

