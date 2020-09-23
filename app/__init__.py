######## IMPORTS ########

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


######## INITIALIZING APP & DATABASE #########

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


from app.controllers import *

@app.errorhandler(404)
def not_found(error):
    return 'Seems like you are lost !'

db.create_all()
