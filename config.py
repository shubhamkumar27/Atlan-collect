###### IMPORTS ######

import os


####### CONFIGURATIONS DEFINED ########
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 
CELERY_BROKER_URL='redis://redis',
CELERY_RESULT_BACKEND='redis://redis'
SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
