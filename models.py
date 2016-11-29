import dateutil.parser

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class SimulationTask(Base):
    """
        Takes Tasks so that requsts can work async
        We can track the status
            Status: NOTSTART
                    STARTED
                    PROCESSING
    """
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    total_investment = Column(Float)
    no_of_days = Column(Integer)
    areas_no = Column(Integer)
    no_of_kms = Column(Integer)
    petrol_price = Column(Float)
    disel_price = Column(Float)
    lpg_price = Column(Float)
    no_of_drivers = Column(Integer)
    drive_time_per_drver = Column(Float)
    driver_salary = Column(Float)
    lpg_cars_no = Column(Integer)
    petrol_cars_no = Column(Integer)
    disel_cars_no = Column(Integer)
    avg_maint_cost = Column(Float)
    avg_petrol_maint = Column(Float)
    avg_disel_maint = Column(Float)
    avg_lpg_maint = Column(Float)


    def __init__(self,kwargs):
        self.status = 'NOTSTART'
        self.total_investment = int(kwargs['total_investment'])
        self.no_of_days = int(kwargs['no_of_days'])
        self.areas_no = int(kwargs['areas_no'])
        self.no_of_kms = int(kwargs['no_of_kms'])
        self.petrol_price = float(kwargs['petrol_price'])
        self.disel_price = float(kwargs['disel_price'])
        self.lpg_price = float(kwargs['lpg_price'])
        self.no_of_drivers = int(kwargs['no_of_drivers'])
        self.drive_time_per_drver = float(kwargs['drive_time_per_drver'])
        self.driver_salary  = float(kwargs['driver_salary'])
        self.lpg_cars_no = int(kwargs['lpg_cars_no'])
        self.petrol_cars_no = int(kwargs['petrol_cars_no'])
        self.disel_cars_no = int(kwargs['disel_cars_no'])
        self.avg_maint_cost = float(kwargs['avg_maint_cost'])
        self.avg_petrol_maint = float(kwargs['avg_petrol_maint'])
        self.avg_disel_maint = float(kwargs['avg_disel_maint'])
        self.avg_lpg_maint = float(kwargs['avg_lpg_maint'])


    def __repr__(self):
        return '<SimulationTask %r>' % (self.id)

class ResultsPerDay(Base):
    """
    Storing Results per Day
    """
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    driver_cost = Column(Float)
    car_cost = Column(Float)
    cars = Column(Integer)
    customer_profit = Column(Float)

    def __init__(self, driver_cost, car_cost, cars, customer_profit):
        self.driver_cost = driver_cost
        self.car_cost = car_cost
        self.cars = cars
        self.customer_profit = customer_profit

    def __repr__(self):
        return '<ResultsPerDay %r>' % (self.id)


class AdminUser(object):
    """
    User Object Gives Info to Flask-adminLTE User Info.
    """
    full_name = "Rido Taxi"
    avatar = "/static/img/taxi.png"
    created_at = dateutil.parser.parse("November 28, 2016")

            
