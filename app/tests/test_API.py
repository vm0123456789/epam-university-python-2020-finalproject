import unittest
import requests
import pytest

BASE = "http://127.0.0.1:5000"


# =========== EmployeeApi and EmployeeByIdApi TESTING ==========

EmployeeApi_URL = f'{BASE}/api/employees'
EMPL_JSON = {
    "name": "John Snow",
    "birthday": "1900-01-01",
    "salary": 1000,
    "department_id": 3
}
empl_id = None

class EmployeeApiTest(unittest.TestCase):

    # GET request to /api/employees returns all employees of the company
    @pytest.mark.order(1)
    def test_1_get_all_employees(self):
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 10)

    # POST request to /api/employees creates new employee
    @pytest.mark.order(2)
    def test_2_create_employee(self):
        r = requests.post(EmployeeApi_URL, json=EMPL_JSON)
        # we store id of newly created employee as global variable
        global empl_id
        empl_id = r.json()['id']
        self.assertEqual(r.status_code, 201)

    # GET newly created employee
    @pytest.mark.order(3)
    def test_3_get_created_employee(self):
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.status_code, 200)
        # check if returned id is equal to the id of previously created object stored as empl_id global variable
        self.assertEqual(r.json()['id'], empl_id)

    # PUT request in order to update recently added employee
    @pytest.mark.order(4)
    def test_4_update_created_employee(self):
        updated_field = {"birthday": "1920-01-01"}
        r = requests.put(f'{EmployeeApi_URL}/{empl_id}', json=updated_field)
        self.assertEqual(r.status_code, 200)
        # GET updated employee and check updated field
        r = requests.get(f'{EmployeeApi_URL}/{empl_id}')
        self.assertEqual(r.json()['birthday'], updated_field["birthday"])

    # DELETE created employee
    @pytest.mark.order(5)
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
dates_range_sales = {"start_date": "1960-01-01", "end_date": "1970-01-01"}  # 2 employees

class SearchApiTest(unittest.TestCase):

    @pytest.mark.order(6)
    def test_6_search_all_employees_by_birthday(self):

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

    @pytest.mark.order(7)
    def test_7_search_employee_by_department_and_birthday(self):
        # id of Sales department is 1. There are 2 employees with birthday between 1960-01-01 and 1970-01-01
        r = requests.get(f'{SearchApi_URL}/1', json=dates_range_sales)
        self.assertEqual(len(r.json()), 2)


# ============ DepartmentApi and DepartmentByIdApi TESTING =============

DepartmentApiURL = f"{BASE}/api/departments"
DEP_JSON = {
    "name": "Human Resources"
}

NEW_EMPLOYEES_JSON = [
    {
        "name": "John Snow",
        "birthday": "1900-01-01",
        "salary": 1000,
        "department_id": 4
    },
    {
        "name": "George Snow",
        "birthday": "1901-01-01",
        "salary": 1500,
        "department_id": 4
    }
]


class DepartmentApiTest(unittest.TestCase):

    # GET request to /api/departments returns all departments of the company
    @pytest.mark.order(8)
    def test_8_get_all_departments(self):
        r = requests.get(DepartmentApiURL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 3)

    # POST request to /api/departments
    @pytest.mark.order(9)
    def test_9_create_department(self):
        r = requests.post(DepartmentApiURL, json=DEP_JSON)
        self.assertEqual(r.status_code, 201)
        # get all departments, should be 4 now
        r = requests.get(DepartmentApiURL)
        self.assertEqual(len(r.json()), 4)

    # Sales department has 5 employees
    @pytest.mark.order(10)
    def test_10_employees_of_the_department(self):
        r = requests.get(f'{DepartmentApiURL}/1')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['employees']), 5)

    '''
    !!! Test is commented out because it fails when running by using  'pytest' command, 
    but passes when tests are running one by one !!!
    Also testing through postman works fine with this put method 
    '''
    # PUT request to update department's name
    @pytest.mark.order(11)
    def test_11_update_department_name(self):
        updated_field = {"name": "Human Resources (HR)"}
        r = requests.put(f'{DepartmentApiURL}/4', json=updated_field)
        self.assertEqual(r.status_code, 200)
        r = requests.get(f'{DepartmentApiURL}/4')
        self.assertEqual(r.json()['name'], updated_field['name'])

        # if we try to update department's name to the name that already exists it should be 412 status code
        r = requests.put(f'{DepartmentApiURL}/4', json={"name": "Sales"})
        self.assertEqual(r.status_code, 412)

    # DELETE created department
    @pytest.mark.order(12)
    def test_12_delete_department(self):
        # create two employees in new department
        for empl in NEW_EMPLOYEES_JSON:
            requests.post(EmployeeApi_URL, json=empl)
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(len(r.json()), 12)
        r = requests.get(f'{DepartmentApiURL}/4')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['employees']), 2)

        # delete department with all employees
        r = requests.delete(f'{DepartmentApiURL}/4')
        self.assertEqual(r.status_code, 204)
        r = requests.get(f'{DepartmentApiURL}/4')
        self.assertEqual(r.status_code, 404)
        r = requests.get(EmployeeApi_URL)
        self.assertEqual(len(r.json()), 10)

# if __name__ == '__main__':
#     unittest.main()


