import requests
import json
from flask import render_template, request, redirect, url_for, jsonify

from app import app
from app.models import Department

from .rest import DepartmentApi

# ========= SUPPLEMENTARY =========

BASE = 'http://localhost:5000'

@app.context_processor
def global_variables():
    return dict(COMPANY_NAME="Dunder Mifflin Paper Company Inc. Scranton Branch departments")


# ========== API REQUESTS FUNCTIONS ============

def get_all_departments():
    """
    :return: departments data in json format. Keys: {id', 'name', 'employees', 'average_salary'}
    """
    return requests.get(f'{BASE}/api/departments').json()


def get_department_employees(dep_name):
    """
    :return: employees data in json format. Keys: {'id', 'name', 'birthday', 'salary', 'department_id}
    """
    dep_id = Department.query.filter_by(name=dep_name).first_or_404().id
    return requests.get(f'{BASE}/api/departments/{dep_id}').json()['employees']

def get_employee(empl_id):
    """
    :return: employee data in json format. Keys: {'id', 'name', 'birthday', 'salary', 'department_id'}
    """
    return requests.get(f'{BASE}/api/employees/{empl_id}').json()

def post_department(data):
    return requests.post(f'{BASE}/api/departments', data).json()

def delete_department(dep_id):
    return requests.delete(f'{BASE}/api/departments/{dep_id}')


# ========= VIEWS ==============

@app.route('/', methods=['GET', 'POST', 'DELETE'])
@app.route('/departments', methods=['GET', 'POST', 'DELETE'])
def departments():
    if request.method == 'GET':
        departments = get_all_departments()
        return render_template('departments.html', title=global_variables()['COMPANY_NAME'],
                               departments=departments)
    elif request.method == 'POST':
        data = request.form
        post_department(data)
    elif request.method == 'DELETE':
        dep_id = int(request.data)
        delete_department(dep_id)
    return redirect(url_for('departments'), 303)







@app.route('/departments/<string:dep_name>')
def department(dep_name):
    employees = get_department_employees(dep_name)
    departments = get_all_departments()
    return render_template('department.html', title=dep_name.capitalize(),
                           employees=employees, departments=departments)


@app.route('/employees/<int:empl_id>')
def employee(empl_id):
    departments= get_all_departments()
    empl = get_employee(empl_id)
    return render_template('employee.html', title=empl['name'], empl=empl, departments=departments)


