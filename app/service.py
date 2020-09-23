############### IMPORTS #################
from flask import render_template, jsonify
from celery.app.task import Task
from app import app, db
from app.models import Task_status
from app.celery_tasks import long_task
from datetime import datetime


############ ALL SERVICES AVAILABLE IN OUR APP ##############

def homeview():
    return render_template('index.html')


def taskview():
    return render_template('tasks.html')


def get_data():
    data = Task_status.query.order_by(Task_status.sno.desc()).limit(10).all()
    return jsonify([i.serialize for i in data])


def upload_file(channel):
    task_status = Task_status(task_id='Not Assigned', data_type = channel, status='QUEUED', time=datetime.now())
    db.session.add(task_status)
    db.session.commit()
    res = long_task.delay(task_status.sno, channel)
    return 'You are going to start a long process !'


def pause_task(tid):
    Task.update_state(self=long_task, task_id=tid, state='PAUSING')
    return 'Your task will be paused !'


def resume_task(tid):
    Task.update_state(self=long_task, task_id=tid, state='RESUME')
    return 'Your task will be resumed !'


def cancel_task(tid):
    Task.update_state(self=long_task, task_id=tid, state='CANCEL')
    return 'Your task will be cancelled !'


def tasks_done():
    data = Task_status.query.filter((Task_status.status=='COMPLETED') | (Task_status.status=='CANCELLED')).all()
    return jsonify([data[i].serialize for i in range(len(data)-1, -1, -1)])



