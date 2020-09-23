########### IMPORTS #############
from app.make_celery import make_celery
from app.models import Task_status, Offline_sales, Online_sales
from app import app, db
import time
import csv


######### CREATING CELERY ###########
celery = make_celery(app)


####### ADDRESS OF CSV FILE #########
base_address = app.config['BASE_DIR']
file_address = base_address+'/app/resources/records.csv'


@celery.task(name='app.long_task', bind=True)
def long_task(self, sno, channel):


    ######### STARTING THE TASK ##########
    task_status = Task_status.query.get(sno)
    task_status.task_id = self.request.id
    self.update_state(state='PROCESSING')
    task_status.status = 'PROCESSING'
    db.session.commit()


    ########## READING CSV FILE ##########
    with open(file_address,'rt')as f:
        data = csv.reader(f)
        for row in data:


            ########### CHECKING FOR PAUSE ###########
            while celery.AsyncResult(self.request.id).state == 'PAUSING' or celery.AsyncResult(self.request.id).state == 'PAUSED':
                if celery.AsyncResult(self.request.id).state == 'PAUSING':
                    print(self.request.id + 'PAUSED')
                    self.update_state(state='PAUSED')
                    task_status.status = 'PAUSED'
                    db.session.commit()

            ########### CHECKING FOR RESUME ###########
            if celery.AsyncResult(self.request.id).state == 'RESUME':
                print(self.request.id + 'RESUMED')
                self.update_state(state='PROCESSING')
                task_status.status = 'PROCESSING'
                db.session.commit()

            ########### CHECKING FOR CANCEL ###########
            if celery.AsyncResult(self.request.id).state == 'CANCEL':
                print(self.request.id + 'CANCELLED')
                self.update_state(state='CANCELLED')
                db.session.rollback()
                task_status.status = 'CANCELLED'
                db.session.commit()
                return 'CANCELLED'

            
            ###################### ADDING INTO DATABASE #######################
            if channel=='offline' and str(row[2])=='Offline':
                offline = Offline_sales(country=str(row[0]), item=str(row[1]), date=str(row[3]), units=str(row[4]))
                db.session.add(offline)

            elif channel=='online' and str(row[2])=='Online':
                online = Online_sales(country=str(row[0]), item=str(row[1]), date=str(row[3]), units=str(row[4]))
                db.session.add(online)


            # time.sleep(0.5)
        db.session.commit()
    

    task_status.status = 'COMPLETED'
    db.session.commit()
    return 'COMPLETED'