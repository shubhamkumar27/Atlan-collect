######## IMPORTS ########

from flask import request
from . import app
from app.service import *


######### ALL THE ROUTES OR APIs WORKING BEHIND #########

@app.route('/')
def home():
    return homeview()


@app.route('/tasks')
def tasks():
    return taskview()


@app.route('/data')
def data():
    return get_data()


@app.route('/upload')
def upload():
    channel = request.args.get('channel')
    return upload_file(channel)


@app.route('/pause')
def pause():
    task_id = request.args.get('id')
    return pause_task(task_id)


@app.route('/resume')
def resume():
    task_id = request.args.get('id')
    return resume_task(task_id)


@app.route('/cancel')
def cancel():
    task_id = request.args.get('id')
    return cancel_task(task_id)


@app.route('/alltasks')
def alltasks():
    return tasks_done()


