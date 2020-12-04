import requests
import json
from flask import render_template, request, redirect, url_for, flash

from app import app
from app.models import Department, Employee

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


def dep_name_by_empl_id(empl_id):
    dep_id = Employee.query.filter_by(id=empl_id).first_or_404().department_id
    return Department.query.filter_by(id=dep_id).first_or_404().name


# ========= DEPARTMENTS VIEWS FUNCTIONS ==============

@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'GET':
        departments = get_all_departments()
        return render_template('departments.html', title=global_variables()['COMPANY_NAME'],
                               departments=departments)
    elif request.method == 'POST':
        data = request.form
        requests.post(f'{BASE}/api/departments', data)
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


# ================== EMPLOYEES VIEW FUNCTIONS ====================

@app.route('/departments/<string:dep_name>', methods=['GET', 'POST'])
def department(dep_name):
    if request.method == 'GET':
        employees = get_department_employees(dep_name)
        departments = get_all_departments()
        return render_template('department.html', dep_name=dep_name, title=dep_name,
                               employees=employees, departments=departments)
    elif request.method == 'POST':
        data = request.form
        print(data)
        requests.post(f'{BASE}/api/employees', data)
        return redirect(url_for('department', dep_name=dep_name), 303)


@app.route('/update_employee/<string:empl_id>', methods=['POST'])
def update_employee(empl_id):
    dep_name = dep_name_by_empl_id(empl_id)
    data = request.form
    requests.put(f'{BASE}/api/employees/{empl_id}', data)
    flash('Employee information updated')
    return redirect(url_for('department', dep_name=dep_name), 303)


@app.route('/delete_employee/<int:empl_id>')
def delete_employee(empl_id):
    dep_name = dep_name_by_empl_id(empl_id)
    requests.delete(f'{BASE}/api/employees/{empl_id}')
    flash('Employee deleted')
    return redirect(url_for('department', dep_name=dep_name), 303)


@app.route('/employees/<int:empl_id>')
def employee(empl_id):
    departments = get_all_departments()
    empl = get_employee(empl_id)
    dep_name = dep_name_by_empl_id(empl_id)
    return render_template('employee.html', dep_name=dep_name, title=empl['name'], empl=empl, departments=departments)
