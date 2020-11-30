import requests
from flask import render_template

from app import app

from .rest import DepartmentApi

# ========= SUPPLEMENTARY =========

BASE = 'http://localhost:5000'

@app.context_processor
def global_variables():
    return dict(COMPANY_NAME="Dunder Mifflin Paper Company Inc. Scranton Branch departments")


# ========== API REQUESTS FUNCTIONS ============

def get_all_departments():
    """
    :return: departments data in json format: <'id', 'name', 'emploees', 'average_salary'>
    """
    return requests.get(f'{BASE}/api/departments').json()


# ========= VIEWS ==============

@app.route('/')
@app.route('/departments')
def departments():
    return render_template('departments.html', title=global_variables()['COMPANY_NAME'],
                           departments=get_all_departments())


@app.route('/departments/<string:dep_name>')
def department(dep_name):
    return render_template('department.html', title=dep_name.capitalize(), departments=get_all_departments())



