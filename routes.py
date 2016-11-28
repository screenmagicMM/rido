
from flask import Flask, render_template, request
from flask_adminlte import AdminLTE
from models import AdminUser, Task, Base
from flask_sqlalchemy import SQLAlchemy



def create_rido_application(configfile=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db = SQLAlchemy(app)
    AdminLTE(app)

    current_user = AdminUser()

    @app.before_first_request
    def setup():
        print ("First Executed")
        # Recreate database each time for demo
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)
        db.session.add(Task('First'))
        db.session.add(Task('Second'))
        db.session.commit()

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
        if request.method == 'POST':
            data = request.form # a multidict containing POST data
            print(data)
            
        return u"<br> Success </br>"    

    @app.route('/test')
    def test():
        tasks = db.session.query(Task).all()
        return u"<br>".join([u"{0}: {1}".format(task.name, task.status) for task in tasks])



    return app