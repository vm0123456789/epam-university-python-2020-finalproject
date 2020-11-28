from app import db
from datetime import datetime as dt

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.Integer, db.ForeignKey('department.name'))

    def __init__(self, name, birthday, salary, department_name):
        self.name = name
        self.birthday = dt.strptime(birthday, '%Y-%m-%d')
        self.salary = salary
        self.department_name = department_name

# to create migration 'flask db init' (flask-migrate)
# to apply migration 'flask db migrate', 'flask db upgrade'
