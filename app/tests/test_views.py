import unittest
from app.site.views import *

BASE = "http://localhost:5000"


class ViewsTest(unittest.TestCase):

    # =========== Api Requests functions TESTING ============

    def test_1_get_all_departments(self):
        """Use GET request to '/api/departments' endpoint"""
        departments_json = get_all_departments()
        self.assertEqual(len(departments_json), 3)

    def test_2_get_department_employees(self):
        """Use GET request to '/api/departments/1' endpoint (Sales department)"""
        department_employees_json = get_department_employees('Sales')  # there are 5 employees
        self.assertEqual(len(department_employees_json), 5)






