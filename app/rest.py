from app import db
from flask_restful import Resource, fields, marshal, marshal_with, reqparse
from .models import Department, Employee

# request parser for Employee model
empl_args = reqparse.RequestParser()
empl_args.add_argument('name', type=str, help="Required")
empl_args.add_argument('birthday', type=str, help="Required <%Y-%m-%d>")
empl_args.add_argument('salary', type=int, help="Required")
empl_args.add_argument('department_name', type=str, help="Required")

# request parser for Department model
dep_args = reqparse.RequestParser()
dep_args.add_argument('name', type=str, help="Required")


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
        return result

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
        return new_employee


class EmployeeByIdApi(Resource):

    @marshal_with(employee_fields)
    def get(self, empl_id):
        # Get employee by id
        result = Employee.query.filter_by(id=empl_id).first_or_404()
        return result

    @marshal_with(employee_fields)
    def put(self, empl_id):
        pass

    @marshal_with(employee_fields)
    def delete(self, empl_id):
        # Delete employee by id
        result = Employee.query.filter_by(id=empl_id).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return result


# ========= DEPARTMENT API ==============

class DepartmentApi(Resource):

    @marshal_with(department_fields)
    def get(self):
        # Get all departments
        result = Department.query.all()
        return result

    @marshal_with(department_fields)
    def post(self):
        args = dep_args.parse_args()
        new_department = Department(name=args['name'])
        db.session.add(new_department)
        db.session.commit()
        return new_department


class DepartmentByIdApi(Resource):

    def get(self, dep_id):
        # Get department by id.
        # Return json with department id, department_name, list of employees and average salary
        dep = Department.query.filter_by(id=dep_id).first_or_404()
        result = marshal(dep, department_fields)
        empl_list = []
        salary_list = []
        for empl in EmployeeApi.get(self):
            if empl['department_name'] == dep.name:
                empl_list.append(empl)
                salary_list.append(empl['salary'])
        result['employees'] = empl_list
        try:
            result['average_salary'] = sum(salary_list)/len(salary_list)
        except ZeroDivisionError:
            result['average_salary'] = 0
        return result


