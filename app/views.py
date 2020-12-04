import requests
import json
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.models import Department

from .rest import DepartmentApi

# ========= SUPPLEMENTARY =========

BASE = 'http://localhost:5000'

@app.context_processor
def global_variables():
    return dict(COMPANY_NAME="Dunder Mifflin Paper Company Inc. Scranton Branch")


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


# ========= DEPARTMENT VIEWS ==============

@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'GET':
        departments = get_all_departments()
        return render_template('departments.html', title=global_variables()['COMPANY_NAME'],
                               departments=departments)
    elif request.method == 'POST':
        data = request.form
        post_department(data)
        flash('Department added')
    return redirect(url_for('departments'), 303)


@app.route('/delete_department/<int:dep_id>')
def delete_department(dep_id):
    requests.delete(f'{BASE}/api/departments/{dep_id}')
    flash('Department deleted')
    return redirect(url_for('departments'), 303)


@app.route('/update_department/<int:dep_id>', methods=['POST'])
def update_department(dep_id):
    data = request.form
    requests.put(f'{BASE}/api/departments/{dep_id}', data)
    flash('Department updated')
    return redirect(url_for('departments'), 303)


@app.route('/departments/<string:dep_name>', methods=['GET'])
def department(dep_name):
    if request.method == 'GET':
        employees = get_department_employees(dep_name)
        departments = get_all_departments()
        return render_template('department.html', title=dep_name,
                               employees=employees, departments=departments)


@app.route('/employees/<int:empl_id>')
def employee(empl_id):
    departments= get_all_departments()
    empl = get_employee(empl_id)
    return render_template('employee.html', title=empl['name'], empl=empl, departments=departments)


