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

empl_id = None

class EmployeeApiTest(unittest.TestCase):

    # GET request to /api/employees returns all employees of the company
    def test_1_get_all_employees(self):
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 10)

    # POST request to /api/employees creates new employee
    def test_2_create_employee(self):
        r = requests.post(EmployeeApi_URL, json=EMPL_OBJ)
        # we store id of newly created employee as global variable
        global empl_id
        empl_id = r.json()['id']
        self.assertEqual(r.status_code, 201)

    # GET newly created employee
    def test_3_get_created_employee(self):
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 200)
        # check if returned id is equal to the id of previously created object stored as empl_id global variable
        self.assertEqual(r.json()['id'], empl_id)

    # PUT request in order to update recently added employee
    def test_4_update_created_employee(self):
        updated_field = {"birthday": "1920-01-01"}
        r = requests.put(f'{EmployeeApi_URL}/{empl_id}', json=updated_field)
        self.assertEqual(r.status_code, 200)
        # GET updated employee and check updated field
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.json()['birthday'], updated_field["birthday"])


if __name__ == '__main__':
    unittest.main()


