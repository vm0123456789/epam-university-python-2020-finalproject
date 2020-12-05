from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
import logging
from logging.handlers import RotatingFileHandler
import os



db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.models import Employee, Department
    db.init_app(app)
    migrate.init_app(app, db)

    from app.site import bp as site_bp
    app.register_blueprint(site_bp)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from app.rest import bp as rest_bp

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/departments_app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('departments_app')

    from app.rest.api import EmployeeApi, EmployeeByIdApi, DepartmentApi, DepartmentByIdApi, SearchApi, SearchByDepartmentApi

    restServ = Api(app)
    restServ.add_resource(EmployeeApi, '/api/employees')
    restServ.add_resource(EmployeeByIdApi, '/api/employees/<int:empl_id>')
    restServ.add_resource(DepartmentApi, '/api/departments')
    restServ.add_resource(DepartmentByIdApi, '/api/departments/<int:dep_id>')
    restServ.add_resource(SearchApi, '/api/search')
    restServ.add_resource(SearchByDepartmentApi, '/api/search/<int:dep_id>')

    return app

from app import models





