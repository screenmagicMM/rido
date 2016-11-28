
from flask import Flask, render_template, request, Response
from flask import jsonify
from flask_adminlte import AdminLTE
from models import AdminUser, SimulationTask, Base
from concurrent.futures import ThreadPoolExecutor
import sys
import json
from models import db_session, engine, Base
from tasks import run_long_task


#Only One Task per time
executor = ThreadPoolExecutor(1)
task_future = None
    




def create_rido_application(configfile=None):
    app = Flask(__name__)
    AdminLTE(app)

    current_user = AdminUser()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

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