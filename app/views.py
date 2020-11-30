import requests
from flask import render_template

from app import app

from .rest import DepartmentApi

# ========= SUPPLEMENTARY =========

BASE = 'http://localhost:5000'

@app.context_processor
def global_variables():
    return dict(COMPANY_NAME="Dunder Mifflin Paper Company Inc. Scranton Branch departments")


# ========= VIEWS ==============

@app.route('/')
@app.route('/departments')
def departments():
    departments = requests.get(f'{BASE}/api/departments').json()
    return render_template('departments.html', title=global_variables()['COMPANY_NAME'],
                           departments=departments)


