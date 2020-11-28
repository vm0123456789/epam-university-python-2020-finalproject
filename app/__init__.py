from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .rest import EmployeeApi, EmployeeByIdApi, DepartmentApi, DepartmentByIdApi

restServ = Api(app)
restServ.add_resource(EmployeeApi, '/api/employees')
restServ.add_resource(EmployeeByIdApi, '/api/employees/<int:empl_id>')
restServ.add_resource(DepartmentApi, '/api/departments')
restServ.add_resource(DepartmentByIdApi, '/api/departments/<int:dep_id>')

from app import views

