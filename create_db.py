from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
import random
from faker import Faker

fake = Faker('ru_RU')  

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'Employees'
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    department = Column(String)
    position = Column(String)
    age = Column(Integer)
    hire_date = Column(Date)

class Salary(Base):
    __tablename__ = 'Salaries'
    salary_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employees.employee_id'))
    base_salary = Column(Float)
    bonus = Column(Float)
    indexation = Column(Float)
    effective_date = Column(Date)

class Forecast(Base):
    __tablename__ = 'Forecasts'
    forecast_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('Employees.employee_id'))
    predicted_indexation = Column(Float)
    predicted_bonus = Column(Float)
    forecast_date = Column(Date)

engine = create_engine('sqlite:///employees.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

departments = ['Финансы', 'Маркетинг', 'ИТ', 'Бухгалтерия', 'Продажи', 'Логистика', 'Кадры']
positions = ['Финансовый аналитик', 'Маркетолог', 'Разработчик', 'Бухгалтер', 'Менеджер по продажам', 'Логист', 'HR-менеджер', 'Системный администратор']

employees = []
for _ in range(5000):
    employee = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        department=random.choice(departments),
        position=random.choice(positions),
        age=random.randint(22, 65),
        hire_date=fake.date_between(start_date='-10y', end_date='today')
    )
    employees.append(employee)

session.add_all(employees)
session.commit()

salaries = []
for employee in employees:
    salary = Salary(
        employee_id=employee.employee_id,
        base_salary=round(random.uniform(30000, 150000), 2),
        bonus=round(random.uniform(2000, 20000), 2),
        indexation=round(random.uniform(2.0, 10.0), 1),
        effective_date=datetime.date(2023, 1, 1)
    )
    salaries.append(salary)

session.add_all(salaries)
session.commit()

forecasts = []
for employee in employees:
    forecast = Forecast(
        employee_id=employee.employee_id,
        predicted_indexation=round(random.uniform(2.0, 10.0), 1),
        predicted_bonus=round(random.uniform(2000, 20000), 2),
        forecast_date=datetime.date(2024, 1, 1)
    )
    forecasts.append(forecast)

session.add_all(forecasts)
session.commit()

session.close()
