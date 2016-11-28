
from flask import Flask, render_template, request, Response
from flask import jsonify
from flask_adminlte import AdminLTE
from models import AdminUser, SimulationTask, Base
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import sys
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

#Only One Task per time
executor = ThreadPoolExecutor(1)
task_future = None
    

def run_long_task(data):
    global db_session, engine
    SimulationTask.__table__.drop(bind=engine)
    SimulationTask.__table__.create(bind=engine)
    db_session.commit()
    print("Simulation Task started!")
    sleep(10)
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
    print("Simulation Task is done!")

def create_rido_application(configfile=None):
    app = Flask(__name__)
    AdminLTE(app)

    current_user = AdminUser()



    @app.before_first_request
    def setup():
        print ("First Executed")
        # Recreate database each time for demo
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        #db.session.add(SimulationTask('First'))
        #db.session.add(SimulationTask('Second'))
        db_session.commit()
        print ('comited happened')

    @app.route('/')
    def index():
        return render_template('index.html', current_user=current_user)

    @app.route('/input')
    def input():
        return render_template('input.html', current_user=current_user)

    @app.route('/login')
    def login():
        return render_template('login.html', current_user=current_user)

    @app.route('/lockscreen')
    def lockscreen():
        return render_template('lockscreen.html', current_user=current_user)

    @app.route('/simulation', methods=['POST'])
    def simulation():
        global task_future
        if task_future == None or task_future.running() != True:
            if request.method == 'POST':
                try:
                    data = request.form # a multidict containing POST data
                    task_future = executor.submit(run_long_task, data)
                    return jsonify(response=200,Status="success")
                except Exception as e:
                    print(e)
                    return jsonify(response=400, Statis="exception")
        else:
            return jsonify(response=400,Status="Task In Progress Rejecting Input")


    @app.route('/test')
    def test():
        tasks = db_session.query(SimulationTask).all()
        return u"<br>".join([u"{0}: {1}".format(task.id, task.status) for task in tasks])



    return app