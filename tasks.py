from celery import Celery
import time
from flask_celery import make_celery
from celery.app.task import Task
# from celery.app.task import Task
# import celery

app = Celery('tasks', broker='amqp://localhost', backend='db+sqlite:///db.sqlite3')
celery = make_celery(app)


@app.task
def reverse(text):
    time.sleep(20)
    return text[::-1]


@app.task
def add():
    time.sleep(10)
    return 3+2


@app.task(bind=True)
def long_task(self):
    print('task_id =' + str(self.request.id))
    self.update_state(state='PROCESSING')
    t = 120
    while(t):
        while app.AsyncResult(self.request.id).state == 'PAUSING' or app.AsyncResult(self.request.id).state == 'PAUSED':
            if app.AsyncResult(self.request.id).state == 'PAUSING':
                print('PAUSED')
                self.update_state(state='PAUSED')
        if app.AsyncResult(self.request.id).state == 'RESUME':
            print('RESUMED')
            self.update_state(state='PROCESSING')
        time.sleep(1)
        t-=1
        # print(self.state)
        
    return 'COMPLETED'


def go():
    global taskid
    worker = long_task.delay()
    taskid = worker.task_id
    return worker.task_id


def pause():
    global taskid
    Task.update_state(self=app, task_id=taskid, state='PAUSING')
    return app.AsyncResult(taskid).state


def resume():
    global taskid
    Task.update_state(self=app, task_id=taskid, state='RESUME')
    return app.AsyncResult(taskid).state
