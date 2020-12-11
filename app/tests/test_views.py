import pytest
import unittest
from app.site.views import *

BASE = "http://localhost:5000"


@pytest.mark.usefixtures("app_context")
class ViewsTest(unittest.TestCase):

    # =========== Api Requests functions TESTING ============

    def test_views_get_all_departments(self):
        """The function `get_all_departments` makes GET request to '/api/departments' endpoint"""
        departments_json = get_all_departments()
        self.assertEqual(len(departments_json), 3)

    def test_views_get_department_employees(self):
        """The function `get_department_employees` makes GET request to '/api/departments/<department_id>' endpoint"""
        department_employees_json = get_department_employees('Sales')
        self.assertEqual(len(department_employees_json), 5)

    def test_views_get_employee(self):
        """The function `get_employee` makes GET request to '/api/employees/<employee_id>' endpoint"""
        empl_id = get_department_employees('Sales')[0]['id']  # The first employee should be 'Jim Halpert'
        employee = get_employee(empl_id)
        self.assertEqual(employee['name'], 'Jim Halpert')

    def test_views_dep_name_by_empl_id(self):
        """The function `views_dep_name_by_empl_id` makes 2 db requests through sqlalchemy"""
        empl_id = get_department_employees('Sales')[0]['id']
        dep_name = dep_name_by_empl_id(empl_id)
        self.assertEqual(dep_name, 'Sales')





