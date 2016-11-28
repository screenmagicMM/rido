from models import SimulationTask
from models import db_session, engine, Base
from time import sleep

def insert_post_data_to_db(data):
    try:
        global db_session, engine
        SimulationTask.__table__.drop(bind=engine)
        SimulationTask.__table__.create(bind=engine)
        db_session.commit()
        print("Simulation Task started!")
        sleep(5)
        simdata = {
            "total_investment" : data['total_investment'].split(',')[0],
            "no_of_days" :data['no_of_days'].split(',')[0],
            "areas_no" : data['areas_no'].split(',')[0],
            "no_of_kms" : data['no_of_kms'].split(',')[0],
            "petrol_price" : data['petrol_price'].split(',')[0],
            "disel_price" : data['disel_price'].split(',')[0],
            "lpg_price" : data['lpg_price'].split(',')[0],
            "no_of_drivers" : data['no_of_drivers'].split(',')[0],
            "drive_time_per_drver" : data['drive_time_per_drver'].split(',')[0],
            "lpg_cars_no" : data['lpg_cars_no'].split(',')[0],
            "petrol_cars_no" : data['petrol_cars_no'].split(',')[0],
            "disel_cars_no" : data['disel_cars_no'].split(',')[0],
            "avg_maint_cost" : data['avg_maint_cost'].split(',')[0],
            "avg_petrol_milage" : data['avg_petrol_milage'].split(',')[0],
            "avg_disel_milege" : data['avg_disel_milege'].split(',')[0],
            "avg_lpg_milege" : data['avg_lpg_milege'].split(',')[0]
        }
        print(simdata)
        sim = SimulationTask(simdata)
        db_session.add(sim)
        print ('added')
        db_session.commit()
        print('Simulation Done')
    except Exception as e:
        print(e)

def calculate_tasks():
    try:
        sim = db_session.query(SimulationTask).first()
        print(sim.status)
    except Exception as e:
        print (e)


def run_long_task(data):
    try:
        insert_post_data_to_db(data)
        calculate_tasks()
    except Exception as e:
        print(e)
    
