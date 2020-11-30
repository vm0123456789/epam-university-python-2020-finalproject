from sqlalchemy.exc import IntegrityError

from app import db
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from .models import Department, Employee
from datetime import datetime as dt

# request parser for EmployeeApi
# dates must be in <'%Y-%m-%d'> format
empl_args = reqparse.RequestParser()
empl_args.add_argument('name', type=str)
empl_args.add_argument('birthday', type=str)
empl_args.add_argument('salary', type=int)
empl_args.add_argument('department_id', type=int)

# request parser for DepartmentApi
dep_args = reqparse.RequestParser()
dep_args.add_argument('name', type=str)

# request parser for SearchApi
search_args = reqparse.RequestParser()
search_args.add_argument('start_date', type=str)
search_args.add_argument('end_date', type=str)

# fields for flask-restful serialization using @marshal_with
employee_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'birthday': fields.String,
    'salary': fields.Integer,
    'department_id': fields.Integer
}

department_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

error_fields = {
    'message': fields.String
}

message_fields = {
    'message': fields.String
}
# ======= EMPLOYEE API =========


class EmployeeApi(Resource):

    @marshal_with(employee_fields)
    def get(self):
        # Get all employees
        result = Employee.query.all()
        return result, 200

    @marshal_with(employee_fields)
    def post(self):
        # Create new employee
        args = empl_args.parse_args()
        new_employee = Employee(name=args['name'],
                                birthday=args['birthday'],
                                salary=args['salary'],
                                department_id=args['department_id'])
        db.session.add(new_employee)
        db.session.commit()
        return new_employee, 201


class EmployeeByIdApi(Resource):

    @marshal_with(employee_fields)
    def get(self, empl_id):
        # Get employee by id
        result = Employee.query.filter_by(id=empl_id).first_or_404()
        return result, 200

    @marshal_with(employee_fields)
    def put(self, empl_id):
        # Update employee by id
        args = empl_args.parse_args()
        if args['birthday'] is not None:
            args['birthday'] = dt.strptime(args['birthday'], '%Y-%m-%d').date()
        empl = Employee.query.filter_by(id=empl_id).first_or_404()
        for k, v in args.items():
            if args[k] is not None:
                setattr(empl, k, v)
        db.session.commit()
        return empl, 200

    @marshal_with(employee_fields)
    def delete(self, empl_id):
        # Delete employee by id
        result = Employee.query.filter_by(id=empl_id).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 204


# ========= DEPARTMENT API ==============

class DepartmentApi(Resource):

    def get(self):
        # Get all departments using DepartmentByIdApi get endpoint
        departments = Department.query.all()
        result = []
        for department in departments:
            result.append(DepartmentByIdApi.get(self, department.id)[0])
        return result, 200

    def post(self):
        args = dep_args.parse_args()
        try:
            new_department = Department(name=args['name'])
            db.session.add(new_department)
            db.session.commit()
            return marshal(new_department, department_fields), 201
        except IntegrityError:
            db.session.rollback()
            return marshal({"message": "The department already exists"}, error_fields), 412




class DepartmentByIdApi(Resource):

    def get(self, dep_id):
        # Get department by id.
        # Return json with department id, department name, list of employees and average salary
        dep = Department.query.filter_by(id=dep_id).first_or_404()
        result = marshal(dep, department_fields)
        empl_list = []
        salary_list = []
        for empl in EmployeeApi.get(self)[0]:
            # [0] - bcz endpoint also returns a status code as second element
            if empl['department_id'] == dep_id:
                empl_list.append(empl)
                salary_list.append(empl['salary'])
        result['employees'] = empl_list
        try:
            result['average_salary'] = round(sum(salary_list) / len(salary_list), 2)
        except ZeroDivisionError:
            result['average_salary'] = 0
        return result, 200

    def put(self, dep_id):
        # update department's name
        args = dep_args.parse_args()
        department = Department.query.filter_by(id=dep_id).first_or_404()
        try:
            for k, v in args.items():
                setattr(department, k, v)
            db.session.commit()
            department_renamed = Department.query.filter_by(id=dep_id).first_or_404()
            return marshal(department_renamed, department_fields), 200
        except IntegrityError:
            # department name should be unique
            db.session.rollback()
            return marshal({"message": "The department with this name already exists"}, error_fields), 412


    def delete(self, dep_id):
        """
        method deletes department along with all its employees
        """
        # delete all employees from this department
        employees = Employee.query.filter_by().all()
        for empl in employees:
            if empl.department_id == dep_id:
                db.session.delete(empl)
        db.session.commit()
        # delete department
        department = Department.query.filter_by(id=dep_id).first_or_404()
        db.session.delete(department)
        db.session.commit()
        return marshal({"message": "The department and all its employees deleted"}, message_fields), 204


# ========= SEARCH API ==============

class SearchApi(Resource):
    @marshal_with(employee_fields)
    def get(self):
        # Get all employees by birthday date / period of dates
        args = search_args.parse_args()
        start_date = dt.strptime(args['start_date'], '%Y-%m-%d').date()
        end_date = dt.strptime(args['end_date'], '%Y-%m-%d').date()
        # get all employees
        employees = Employee.query.all()
        # filter employees by birthday
        employees = [empl for empl in employees if start_date <= empl.birthday <= end_date]
        return employees, 200

class SearchByDepartmentApi(Resource):

    @marshal_with(employee_fields)
    def get(self, dep_id):
        # Get employees of the department by birthday date / period of dates
        args = search_args.parse_args()
        start_date = dt.strptime(args['start_date'], '%Y-%m-%d').date()
        end_date = dt.strptime(args['end_date'], '%Y-%m-%d').date()
        # get all employees of the department
        employees = Employee.query.filter_by(department_id=dep_id).all()
        # filter employees by birthday
        employees = [empl for empl in employees if start_date <= empl.birthday <= end_date]
        return employees, 200
