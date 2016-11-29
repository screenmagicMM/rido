
from flask import Flask, render_template, request, Response
from flask import jsonify
from flask_adminlte import AdminLTE
from models import AdminUser, SimulationTask, ResultsPerDay, Base
from concurrent.futures import ThreadPoolExecutor
import sys
import json
from models import db_session, engine, Base
from tasks import run_long_task
from tasks import print_exception
from sqlalchemy import func
import logging
import logging.config
from config import g_logger


#Only One Task per time
executor = ThreadPoolExecutor(1)
task_future = None



    
#Main function contains multiple routes
def create_rido_application(configfile=None):
    app = Flask(__name__)
    AdminLTE(app)

    current_user = AdminUser()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()



    @app.before_first_request
    def setup():
        g_logger.info ("First Time Creating Local DB")
        # Recreate database each time for demo
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        #db.session.add(SimulationTask('First'))
        #db.session.add(SimulationTask('Second'))
        db_session.commit()
        g_logger.info ('DB Created ')



    @app.route('/')
    def index():
        sim = db_session.query(SimulationTask).first()
        g_logger.debug('---> {}'.format(sim))
        try:
            if not sim == None:
                if sim.status == 'DONE':
                    data = dict()
                    results = db_session.query(ResultsPerDay).all()
                    #We stored database per day
                    #inorder to get total we sum driver_cost, car_cost, customer_profit
                    sumdrv, sumcar, sumcus = db_session.query(func.sum(ResultsPerDay.driver_cost),
                                            func.sum(ResultsPerDay.car_cost),
                                            func.sum(ResultsPerDay.customer_profit)).first()
                    data['investment'] = sim.total_investment
                    data['drivercost']= "{0:.2f}".format(sumdrv)
                    data['carcost']= "{0:.2f}".format(sumcar)
                    investment = sim.total_investment
                    profit = (investment + sumcus) - (sumdrv + sumcar)
                    g_logger.debug('--> Profit {} '.format(profit))
                    g_logger.debug('--> Total investment{} '.format(investment))
                    g_logger.debug('--> Customer income{}'.format(sumcus))
                    g_logger.debug('---> Driver Expense {}'.format(sumdrv))
                    g_logger.debug('---> Car Expense {}'.format(sumcar))
                    
                    data['profit'] = "{0:.2f}".format(profit)
                    data['customer_income'] = "{0:.2f}".format(sumcus)

                    #prepare Chart Data
                    labels = []
                    dcost = []
                    ccost = []
                    for x in results:
                        labels += [int(x.id)]
                        dcost += [x.driver_cost]
                        ccost += [x.car_cost/100]

                    cdata = [dcost,ccost]

                    g_logger.debug('----> {}'.format(labels))
                    g_logger.debug('----> {}'.format(cdata))
                    return render_template('index.html', current_user = current_user, results = data, 
                                          chartlabel = labels, chartdata= cdata,profit=profit, 
                                          carexpenses=sumcar, driverexpenses=sumdrv, nodays=sim.no_of_days)
                else:
                    return render_template('lockscreen.html', current_user=current_user)
            else:
                return render_template('lockscreen.html', current_user=current_user)
        except Exception as e:
            print_exception()
            return render_template('lockscreen.html', current_user=current_user)


    @app.route('/input')
    def input():
        return render_template('input.html', current_user=current_user)


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
                    print_exception()
                    return jsonify(response=400, Statis="exception")
        else:
            return jsonify(response=400,Status="reject")
    return app