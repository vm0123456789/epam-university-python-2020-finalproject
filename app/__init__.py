from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .rest import EmployeeApi, EmployeeByIdApi, DepartmentApi, DepartmentByIdApi, SearchApi, SearchByDepartmentApi

restServ = Api(app)
restServ.add_resource(EmployeeApi, '/api/employees')
restServ.add_resource(EmployeeByIdApi, '/api/employees/<int:empl_id>')
restServ.add_resource(DepartmentApi, '/api/departments')
restServ.add_resource(DepartmentByIdApi, '/api/departments/<int:dep_id>')
restServ.add_resource(SearchApi, '/api/search')
restServ.add_resource(SearchByDepartmentApi, '/api/search/<int:dep_id>')

import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/departments_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('departments_app')

from app import views, errors

