import unittest
import requests

BASE = "http://localhost:5000"

# =========== EmployeeApi and EmployeeByIdApi test global variables ==========

EmployeeApi_URL = f'{BASE}/api/employees'
EMPL_JSON = {
    "name": "John Snow",
    "birthday": "1900-01-01",
    "salary": 1000,
    "dep_name": "Warehouse"
}

# ============ SearchApi and SearchbyDepartmentApi test global variables ============

SearchApi_URL = f'{BASE}/api/search'
dates_range_true = {"start_date": "1890-01-01", "end_date": "1910-01-01"}
dates_range_false = {"start_date": "1000-01-01", "end_date": "1500-01-01"}
specific_date_true = {"start_date": "1900-01-01", "end_date": "1900-01-01"}
dates_range_sales = {"start_date": "1960-01-01", "end_date": "1970-01-01"}  # 2 employees

# ============ DepartmentApi and DepartmentByIdApi test global variables =============

DepartmentApiURL = f"{BASE}/api/departments"
DEP_JSON = {
    "name": "Human Resources"
}

NEW_EMPLOYEES_JSON = [
    {
        "name": "John Snow",
        "birthday": "1900-01-01",
        "salary": 1000,
        "dep_name": "Human Resources (HR)"
    },
    {
        "name": "George Snow",
        "birthday": "1901-01-01",
        "salary": 1500,
        "dep_name": "Human Resources (HR)"
    }
]


class ApiTest(unittest.TestCase):

    # =========== EmployeeApi and EmployeeByIdApi TESTING ==========

    def test_1_EmployeeApi_EmployeeByIdApi(self):
        # GET request to /api/employees returns all employees of the company
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 10)

        # POST request to /api/employees creates new employee
        r = requests.post(EmployeeApi_URL, json=EMPL_JSON)
        # we store id of newly created employee as global variable
        empl_id = r.json()['id']
        self.assertEqual(r.status_code, 201)

        # GET newly created employee
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 200)
        # check if returned id is equal to the id of previously created object stored as empl_id global variable
        self.assertEqual(r.json()['id'], empl_id)

        # PUT request in order to update recently added employee
        updated_field = {"birthday": "1920-01-01"}
        r = requests.put(f'{EmployeeApi_URL}/{empl_id}', json=updated_field)
        self.assertEqual(r.status_code, 200)
        # GET updated employee and check updated field
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.json()['birthday'], updated_field["birthday"])

        # DELETE created employee
        r = requests.delete(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 204)
        # GET deleted employee
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 404)

    # ============ SearchApi and SearchbyDepartmentApi TESTING =============

    def test_2_SearchApi_SearchByDepartmentApi(self):
        # create new employee and store employee's id in global variable
        r = requests.post(EmployeeApi_URL, json=EMPL_JSON)
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
        # delete created employee
        r = requests.delete(f'{EmployeeApi_URL}/{empl_id}')

        # Search employee by department and birthday
        # id of Sales department is 1. There are 2 employees with birthday between 1960-01-01 and 1970-01-01
        r = requests.get(f'{SearchApi_URL}/1', json=dates_range_sales)
        self.assertEqual(len(r.json()), 2)

    # ============ DepartmentApi and DepartmentByIdApi TESTING =============

    def test_3_DepartmentApi_DepartmentByIdApi(self):
        # GET request to /api/departments returns all departments of the company
        r = requests.get(DepartmentApiURL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 3)

        # POST request to /api/departments
        r = requests.post(DepartmentApiURL, json=DEP_JSON)
        dep_id = r.json()['id']
        self.assertEqual(r.status_code, 201)
        # get all departments, should be 4 now
        r = requests.get(DepartmentApiURL)
        self.assertEqual(len(r.json()), 4)

        # Sales department has 5 employees
        r = requests.get(f'{DepartmentApiURL}/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['employees']), 5)

        # PUT request to update department's name
        updated_field = {"name": "Human Resources (HR)"}
        r = requests.put(f'{DepartmentApiURL}/{dep_id}', json=updated_field)
        self.assertEqual(r.status_code, 200)
        r = requests.get(f'{DepartmentApiURL}/{dep_id}')
        self.assertEqual(r.json()['name'], updated_field['name'])

        # if we try to update department's name to the name that already exists it should be 412 status code
        r = requests.put(f'{DepartmentApiURL}/{dep_id}', json={"name": "Sales"})
        self.assertEqual(r.status_code, 412)

        # DELETE created department

        # create two employees in new department
        for empl in NEW_EMPLOYEES_JSON:
            requests.post(EmployeeApi_URL, json=empl)
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(len(r.json()), 12)
        r = requests.get(f'{DepartmentApiURL}/{dep_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['employees']), 2)

        # delete department with all employees
        r = requests.delete(f'{DepartmentApiURL}/{dep_id}')
        self.assertEqual(r.status_code, 204)
        r = requests.get(f'{DepartmentApiURL}/{dep_id}')
        self.assertEqual(r.status_code, 404)
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(len(r.json()), 10)

# if __name__ == '__main__':
#     unittest.main()
