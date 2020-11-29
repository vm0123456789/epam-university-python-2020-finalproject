import unittest
import requests

BASE = "http://127.0.0.1:5000"


# =========== EmployeeApi and EmployeeByIdApi TESTING ==========

EmployeeApi_URL = f'{BASE}/api/employees'
EMPL_OBJ = {
    "name": "John Snow",
    "birthday": "1900-01-01",
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

    # DELETE created employee
    def test_5_delete_created_employee(self):
        r = requests.delete(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 204)
        # GET deleted employee
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 404)


# ============ SearchApi and SearchbyDepartmentApi TESTING =============

SearchApi_URL = f'{BASE}/api/search'
dates_range_true = {"start_date": "1890-01-01", "end_date": "1910-01-01"}
dates_range_false = {"start_date": "1000-01-01", "end_date": "1500-01-01"}
specific_date_true = {"start_date": "1900-01-01", "end_date": "1900-01-01"}

class SearchApiTest(unittest.TestCase):

    def test_6_search_all_employees_by_birthday(self):

        # create new employee and store employee's id in global variable
        r = requests.post(EmployeeApi_URL, json=EMPL_OBJ)
        global empl_id
        empl_id = r.json()['id']

        # employee's birthday within the range
        r = requests.get(SearchApi_URL, json=dates_range_true)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['id'], empl_id)

        # employee's birthday out of range
        r = requests.get(SearchApi_URL, json=dates_range_false)
        self.assertEqual(r.status_code, 200)  # empty list returned
        self.assertEqual(r.json(), [])

        # employee's birthday date
        r = requests.get(SearchApi_URL, json=specific_date_true)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['birthday'], specific_date_true['start_date'])

    # def test_7_search_employee_by_department_and_birthday(self):
    #     pass
    #     # employee created in previous test




# if __name__ == '__main__':
#     unittest.main()


