from re import sub
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base


# --------------------------------------------
#             HH.RU VACANCY
#---------------------------------------------

PRODUCT_URL = "https://ekaterinburg.hh.ru/search/vacancy?area=3&employment=full&industry=7&label=not_from_agency&professional_role=10&professional_role=12&professional_role=25&professional_role=34&professional_role=36&professional_role=73&professional_role=96&professional_role=104&professional_role=107&professional_role=112&professional_role=113&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&schedule=fullDay&search_field=name&search_field=company_name&search_field=description&only_with_salary=true&text=%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA&order_by=relevance&search_period=0&items_on_page=50&no_magic=true&L_save_area=true&from=suggest_post"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
page = requests.get(url=PRODUCT_URL, headers=headers)

soup = BeautifulSoup(page.content, "lxml")

vacancy_items_first = soup.find_all(
    "div",
    class_="vacancy-serp-item-body__main-info"
)
first_website = "ekaterinburg.hh.ru"

# --------------------------------------------
#             ZARPLATA.RU VACANCY
#---------------------------------------------

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'device': '29e24340-01c6-11ed-8dee-03df543d76dd',
    'hh-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 (UUID: 29e24340-01c6-11ed-8dee-03df543d76dd) (ZP_FRANCHISE: zarplata)',
    'Origin': 'https://ekb.zarplata.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://ekb.zarplata.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'If-Modified-Since': 'Tue, 12 Jul 2022 09:36:52 +0000',
}

response = requests.get('https://api.zp.ru/v1/collapsed_vacancies?search_type=fullThrottle&q=%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA&professional_role_id[]=10&schedule_id[]=305&working_type_id[]=309&is_notempty_salary=true&average_salary=true&categories_facets=true&highlight=true&state=1&explain=1&geo_id=3&agglomeration_vacancies_count_facets=1&rubric_filter_mode=new', headers=headers)


data = response.json()

vacancy_items_second = data["vacancies"]

second_website = "ekb.zarplata.ru"

# --------------------------------------------
#             БАЗА ДАННЫХ
#---------------------------------------------

Base = declarative_base()

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

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_vacancy(title, salary_from, salary_to, website):
    is_exist = session.query(Vacancy).filter(
        Vacancy.name==title
    ).order_by(Vacancy.datetime.desc()).first()

    if not is_exist:
        session.add(
            Vacancy(
                name=title,
                datetime=datetime.now(),
                salary_from=salary_from,
                salary_to=salary_to,
                website=website
            )
        )
        session.commit()
    else:
        if is_exist.salary_to != salary_to:
            session.add(
                Vacancy(
                    name=title,
                    datetime=datetime.now(),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    website=website
                )
            )
            session.commit()

for item in vacancy_items_first:

    vacancy_title = item.find(
        "span",
        class_="resume-search-item__name"
    ).get_text()

    vacancy_salary = item.find(
        "span", 
        class_="bloko-header-section-3"
    )

    salary_item = vacancy_salary.get_text().split('–')
    salary_item[0] = Decimal(sub(r"[^\d\-.]", "", salary_item[0]))
    if (len(salary_item) > 1):
        salary_item[1] = Decimal(sub(r"[^\d\-.]", "", salary_item[1]))
        add_vacancy(vacancy_title, salary_item[0], salary_item[1], first_website)
    else: 
        add_vacancy(vacancy_title, salary_item[0], 0, first_website)

salary_item_sec=[0, 0]

for item in vacancy_items_second:
    vacancy_title = item["header"]
    salary_item_sec[0] = item["salary_min"]
    salary_item_sec[1]=item["salary_max"]
    if salary_item_sec[1] == None:
        salary_item_sec[1] = 0
    add_vacancy(vacancy_title, salary_item_sec[0], salary_item_sec[1], second_website)


items = session.query(Vacancy).all()
for item in items:
    print(item)


