from models import SimulationTask, ResultsPerDay
from models import db_session, engine, Base
from time import sleep
import linecache
import sys
import random
from config import g_logger


def print_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    g_logger.debug ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def insert_post_data_to_db(data):
    try:
        global db_session, engine
        SimulationTask.__table__.drop(bind=engine)
        SimulationTask.__table__.create(bind=engine)
        db_session.commit()
        g_logger.debug("Simulation Task started!")
        g_logger.debug('{}'.format(data))
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
            "driver_salary" : data['driver_salary'].split(',')[0],
            "lpg_cars_no" : data['lpg_cars_no'].split(',')[0],
            "petrol_cars_no" : data['petrol_cars_no'].split(',')[0],
            "disel_cars_no" : data['disel_cars_no'].split(',')[0],
            "avg_maint_cost" : data['avg_maint_cost'].split(',')[0],
            "avg_petrol_maint" : data['avg_petrol_maint'].split(',')[0],
            "avg_disel_maint" : data['avg_disel_maint'].split(',')[0],
            "avg_lpg_maint" : data['avg_lpg_maint'].split(',')[0]
        }
        g_logger.debug('simdata {}'.format(simdata))
        sim = SimulationTask(simdata)
        db_session.add(sim)
        g_logger.debug ('added')
        db_session.commit()
        g_logger.debug('Simulation Done')
    except Exception as e:
        print_exception()

def calculate_tasks():
    try:
        ResultsPerDay.__table__.drop(bind=engine)
        ResultsPerDay.__table__.create(bind=engine)

        sim = db_session.query(SimulationTask).first()
        sim.status = 'PROCESSING'
        db_session.commit()
        #Per Day
        ndays = sim.no_of_days
        for x in range(1,ndays+1):


            # we assume customer pay
            #PER Drivers
            ndrivers = sim.no_of_drivers
            drv_time_per_driver = sim.drive_time_per_drver;

            total_time_driven_per_day = ndrivers * drv_time_per_driver

            #customers Payment
            # we assume customer may pay some thinglike  (50 to 100 per hour)
            customer_pay_per_hr = random.uniform(50,100)
            # Total customer pays = customer pay * ndrivers * drive_time_per_hr
            r_total_customer_paid = customer_pay_per_hr * total_time_driven_per_day 

            g_logger.debug('      CustomerPay = {}'.format(r_total_customer_paid))
            #Area
            nareas = sim.areas_no
            nkms_perday = sim.no_of_kms
            total_kms_covered_perday = nareas * nkms_perday


            #cars
            nlpg_cars = sim.lpg_cars_no
            npet_cars = sim.petrol_cars_no
            ndis_cars = sim.disel_cars_no
            total_cars = nlpg_cars + npet_cars + ndis_cars
            lpg_car_ratio = nlpg_cars / total_cars
            pet_car_ratio = npet_cars / total_cars
            dis_car_ratio = ndis_cars / total_cars

            pet_car_distance =  total_kms_covered_perday * pet_car_ratio
            lpg_car_distance =  total_kms_covered_perday * lpg_car_ratio
            dis_car_distance =  total_kms_covered_perday * dis_car_ratio

            #cost
            pet_price = sim.petrol_price
            dis_price = sim.disel_price
            lpg_price = sim.lpg_price

            pet_maint = sim.avg_petrol_maint
            dis_maint = sim.avg_disel_maint
            lpg_maint = sim.avg_lpg_maint

            # We assume FuelWastage  
            #basedon 30% Heavy Traffic 40 % normal traffic 20% night traffic
            fuel_wastage_heavy_traffic = 10 * random.uniform(5/100, 30/100)
            fuel_wastage_normal_traffic = 5 * random.uniform(5/100, 40/100)
            fuel_wastage_night_traffic  = 2 * random.uniform(5/100, 20/100)
            total_fuel_wastage = fuel_wastage_heavy_traffic + fuel_wastage_normal_traffic + fuel_wastage_night_traffic

            # Per fuel cost
            petrol_car_cost = pet_price * pet_car_distance + total_fuel_wastage * pet_car_distance
            disel_car_cost = dis_price * dis_car_distance + total_fuel_wastage * dis_car_distance
            lpg_car_cost = lpg_price * lpg_car_distance + total_fuel_wastage * lpg_car_distance

            petrol_car_cost = petrol_car_cost + pet_maint
            disel_car_cost  = disel_car_cost + dis_maint
            lpg_car_cost    = lpg_car_cost + lpg_maint

            total_pet_car_cost = petrol_car_cost * npet_cars
            total_dis_car_cost = disel_car_cost * ndis_cars
            total_lpg_car_cost = lpg_car_cost * nlpg_cars
            total_fuel_cost = total_pet_car_cost + total_dis_car_cost + total_lpg_car_cost

            r_total_car_cost = total_fuel_cost + sim.avg_maint_cost * total_cars

            #we assume we pay total car cost. Drivers are payed per hours
            
            #driver pay per_day = driver_salary * #drivers * #drvtimeperdriver *
            #                     
            pay_perday = sim.driver_salary * ndrivers * drv_time_per_driver
            r_total_driver_cost = pay_perday

            g_logger.debug(' Total driver_cost = {}'.format(r_total_driver_cost))
            g_logger.debug(' Total car Cost = {}'.format(r_total_car_cost))
            r = ResultsPerDay(r_total_driver_cost, r_total_car_cost, total_cars, r_total_customer_paid)
            sim.status='DONE'
            db_session.add(r)
            db_session.commit()


    except Exception as e:
        print_exception()


def run_long_task(data):
    try:
        insert_post_data_to_db(data)
        calculate_tasks()
    except Exception as e:
        print_exception()    
