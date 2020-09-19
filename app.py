from flask import Flask, render_template, request, jsonify, redirect
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy
from celery.app.task import Task
import time
from datetime import datetime

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://localhost',
    CELERY_RESULT_BACKEND='redis://'
)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/tasks'
db = SQLAlchemy(flask_app)


class Tasks_status(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(80), unique=True, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=True)
    status = db.Column(db.String(80), unique=False, nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'sno'         : self.sno,
           'task_id'     : self.task_id,
           'time'        : dump_datetime(self.time),
           'status'      : self.status,
       }


celery = make_celery(flask_app)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%H:%M:%S")+"  "+value.strftime("%d-%m-%Y")

@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/data')
def get_data():
    data = Tasks_status.query.order_by(Tasks_status.sno).all()
    return jsonify([data[i].serialize for i in range(len(data)-1, -1, -1)])


@flask_app.route('/start')
def start():
    global taskid
    task_status = Tasks_status(task_id='Not Assigned', status='QUEUED')
    db.session.add(task_status)
    db.session.commit()
    res = long_task.delay(task_status.sno)
    taskid = str(res.task_id)
    return redirect('/')


@flask_app.route('/pause')
def pause():
    tid = request.args.get('id')
    print(tid)
    Task.update_state(self=long_task, task_id=tid, state='PAUSING')
    return celery.AsyncResult(tid).state


@flask_app.route('/resume')
def resume():
    tid = request.args.get('id')
    print(tid)
    Task.update_state(self=long_task, task_id=tid, state='RESUME')
    return celery.AsyncResult(tid).state


@flask_app.route('/cancel')
def cancel():
    tid = request.args.get('id')
    print(tid)
    Task.update_state(self=long_task, task_id=tid, state='CANCEL')
    return celery.AsyncResult(tid).state


@celery.task(name='app.long_task', bind=True)
def long_task(self, sno):
    print(sno)
    task_status = Tasks_status.query.get(sno)
    task_status.task_id = self.request.id
    print('task_id =' + str(self.request.id))
    self.update_state(state='PROCESSING')
    task_status.status = 'PROCESSING'
    db.session.commit()
    print(celery.AsyncResult(self.request.id).state)
    t = 60
    while(t):
        while celery.AsyncResult(self.request.id).state == 'PAUSING' or celery.AsyncResult(self.request.id).state == 'PAUSED':
            if celery.AsyncResult(self.request.id).state == 'PAUSING':
                print(self.request.id, 'PAUSED')
                self.update_state(state='PAUSED')
                task_status.status = 'PAUSED'
                db.session.commit()
    
        if celery.AsyncResult(self.request.id).state == 'RESUME':
            print(self.request.id, 'RESUMED')
            self.update_state(state='PROCESSING')
            task_status.status = 'PROCESSING'
            db.session.commit()

        if celery.AsyncResult(self.request.id).state == 'CANCEL':
            print(self.request.id, 'CANCELLED')
            self.update_state(state='CANCELLED')
            task_status.status = 'CANCELLED'
            db.session.commit()

        time.sleep(1)
        t -= 1
    
    task_status.status = 'COMPLETED'
    db.session.commit()
    return 'COMPLETED'


if __name__ == "__main__":
    flask_app.run(debug=True)

