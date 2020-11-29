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
empl_args.add_argument('department_name', type=str)

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
    'department_name': fields.String
}

department_fields = {
    'id': fields.Integer,
    'name': fields.String,
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
                                department_name=args['department_name'])
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

    @marshal_with(department_fields)
    def post(self):
        args = dep_args.parse_args()
        new_department = Department(name=args['name'])
        db.session.add(new_department)
        db.session.commit()
        return new_department, 201


class DepartmentByIdApi(Resource):

    def get(self, dep_id):
        # Get department by id.
        # Return json with department id, department_name, list of employees and average salary
        dep = Department.query.filter_by(id=dep_id).first_or_404()
        result = marshal(dep, department_fields)
        empl_list = []
        salary_list = []
        for empl in EmployeeApi.get(self)[0]:
            # [0] - bcz endpoint also returns a status code as second element
            if empl['department_name'] == dep.name:
                empl_list.append(empl)
                salary_list.append(empl['salary'])
        result['employees'] = empl_list
        try:
            result['average_salary'] = round(sum(salary_list) / len(salary_list), 2)
        except ZeroDivisionError:
            result['average_salary'] = 0
        return result, 200

    @marshal_with(department_fields)
    def put(self, dep_id):
        # TODO
        pass

    @marshal_with(department_fields)
    def delete(self, dep_id):
        # TODO delete all employees from the department if the department is deleted
        # delete department by id
        result = Department.query.filter_by(id=dep_id).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result, 204


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
        dep = Department.query.filter_by(id=dep_id).first_or_404()
        employees = Employee.query.filter_by(department_name=dep.name).all()
        # filter employees by birthday
        employees = [empl for empl in employees if start_date <= empl.birthday <= end_date]
        return employees, 200
