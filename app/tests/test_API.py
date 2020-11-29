import unittest
import requests

BASE = "http://127.0.0.1:5000"
EmployeeApi_URL = f'{BASE}/api/employees'
EMPL_OBJ = {
    "name": "John Snow",
    "birthday": "1970-08-08",
    "salary": 1000,
    "department_name": "Warehouse"
}

class EmployeeApiTest(unittest.TestCase):

    # GET request to /api/employees returns all employees of the company
    def test_1_get_all_employees(self):
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 10)

    # POST request to /api/employees creates new employee
    def test_2_post_employee(self):
        r = requests.post(EmployeeApi_URL, json=EMPL_OBJ)
        self.assertEqual(r.status_code, 201)


if __name__ == '__main__':
    unittest.main()


