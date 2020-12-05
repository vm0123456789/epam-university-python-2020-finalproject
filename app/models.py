from datetime import datetime as dt
from app import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __init__(self, name):
        self.name = name

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def __init__(self, name, birthday, salary, department_id):
        self.name = name
        self.birthday = dt.strptime(birthday, '%Y-%m-%d').date()
        self.salary = salary
        self.department_id = department_id

# to create migration 'flask db init' (flask-migrate)
# to apply migration 'flask db migrate', 'flask db upgrade'

