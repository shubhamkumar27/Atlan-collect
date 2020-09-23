########### IMPORTS #############

from app import db
import datetime


########### TABLE FOR TASK STATUS ###########

class Task_status(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(80), unique=False, nullable=False)
    data_type = db.Column(db.String(80), unique=False, nullable=True)
    time = db.Column(db.String(80), unique=False, nullable=True)
    status = db.Column(db.String(80), unique=False, nullable=False)

    @property
    def serialize(self):
       return {
           'sno'         : self.sno,
           'task_id'     : self.task_id,
           'data_type'   : self.data_type,
           'time'        : format_datetime(self.time),
           'status'      : self.status,
       }


########### ONLINE SALES DATA TABLE #############

class Online_sales(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), unique=False, nullable=False)
    item = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    units = db.Column(db.String(80), unique=False, nullable=False)


########### OFFLINE SALES DATA TABLE #############

class Offline_sales(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80), unique=False, nullable=False)
    item = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    units = db.Column(db.String(80), unique=False, nullable=False)


######### FUNCTION TO FORMAT DATE ########

def format_datetime(value):
    if value is None:
        return None
    date, time = value.split(' ')
    d = date.split('-')
    d.reverse()
    date = '-'.join(d)
    t, v = time.split('.')
    return t + '  |  Date : ' + date
