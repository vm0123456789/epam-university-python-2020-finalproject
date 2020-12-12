import pytest
import requests

BASE = "http://localhost:5000"

EmployeeApi_URL = f'{BASE}/api/employees'
DepartmentApiURL = f"{BASE}/api/departments"
SearchApi_URL = f'{BASE}/api/search'

dates_range_true = {"start_date": "1890-01-01", "end_date": "1910-01-01"}
dates_range_false = {"start_date": "1000-01-01", "end_date": "1500-01-01"}
specific_date_true = {"start_date": "1900-01-01", "end_date": "1900-01-01"}
dates_range_sales = {"start_date": "1960-01-01", "end_date": "1970-01-01"}  # 2 employees

new_department = {"name": "Human Resources"}
new_employees = [
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

empl_data = {
    "name": "John Snow",
    "birthday": "1900-01-01",
    "salary": 1000,
    "dep_name": "Warehouse"
}
dep_data = {"name": "Warehouse"}


def test_api_DepartmentApi_DepartmentByIdApi(client):
    # GET request to /api/departments returns all departments of the company
    r = client.get(DepartmentApiURL)
    assert r.status_code == 200
    assert len(r.json) == 0

    # POST request to /api/departments
    r = client.post(DepartmentApiURL, data=new_department)
    dep_id = r.json['id']
    assert r.status_code == 201
    r = client.get(DepartmentApiURL)
    assert len(r.json) == 1

    # PUT request to update department's name
    updated_field = {"name": "Human Resources (HR)"}
    r = client.put(f'{DepartmentApiURL}/{dep_id}', data=updated_field)
    assert r.status_code == 200
    r = client.get(f'{DepartmentApiURL}/{dep_id}')
    assert r.json['name'] == updated_field['name']

    # DELETE created department

    # create two employees in new department
    for empl in new_employees:
        client.post(EmployeeApi_URL, data=empl)
    r = client.get(EmployeeApi_URL)
    assert len(r.json) == 2
    r = client.get(f'{DepartmentApiURL}/{dep_id}')
    assert r.status_code == 200
    assert len(r.json['employees']) == 2

    # delete department with all employees
    r = client.delete(f'{DepartmentApiURL}/{dep_id}')
    assert r.status_code == 204
    r = client.get(f'{DepartmentApiURL}/{dep_id}')
    assert r.status_code == 404
    r = client.get(EmployeeApi_URL)
    assert len(r.json) == 0


# =========== EmployeeApi and EmployeeByIdApi TESTING ==========

def test_api_EmployeeApi_EmployeeByIdApi(client):

    # create department "Warehouse"
    r = client.post(DepartmentApiURL, data=dep_data)
    dep_id = r.json['id']

    # GET request to /api/employees returns all employees of the company
    r = client.get(EmployeeApi_URL)
    assert r.status_code == 200
    assert len(r.json) == 0

    # POST request to /api/employees creates new employee
    r = client.post(EmployeeApi_URL, data=empl_data, follow_redirects=True)
    # we store id of newly created employee as global variable
    empl_id = r.json['id']
    assert r.status_code == 201

    # GET newly created employee
    r = client.get(f'{EmployeeApi_URL}/{empl_id}')
    assert r.status_code == 200
    assert r.json['name'] == 'John Snow'

    # PUT request in order to update recently added employee
    updated_field = {"birthday": "1920-01-01"}
    r = client.put(f'{EmployeeApi_URL}/{empl_id}', data=updated_field)
    assert r.status_code == 200
    # GET updated employee and check updated field
    r = client.get(f'{EmployeeApi_URL}/{empl_id}')
    assert r.json['birthday'] == updated_field['birthday']

    # DELETE created employee
    r = client.delete(f'{EmployeeApi_URL}/{empl_id}')
    assert r.status_code == 204
    # GET deleted employee
    r = client.get(f'{EmployeeApi_URL}/{empl_id}')
    assert r.status_code == 404

    # delete department "Warehouse"
    r = client.delete(f'{DepartmentApiURL}/{dep_id}')
    assert r.status_code == 204

# ============ SearchApi and SearchbyDepartmentApi TESTING =============

def test_api_SearchApi_SearchByDepartmentApi(client):

    # create department "Warehouse"
    r = client.post(DepartmentApiURL, data=dep_data)
    dep_id = r.json['id']

    # create new employee and store employee's id
    r = client.post(EmployeeApi_URL, data=empl_data)
    empl_id = r.json['id']

    # employee's birthday within the range
    r = client.get(SearchApi_URL, data=dates_range_true)
    assert r.status_code == 200
    assert r.json[0]['id'] == empl_id

    # employee's birthday out of range
    r = client.get(SearchApi_URL, data=dates_range_false)
    assert r.status_code == 200
    assert r.json == []  # empty list returned

    # employee's birthday date
    r = client.get(SearchApi_URL, data=specific_date_true)
    assert r.status_code == 200
    assert r.json[0]['birthday'] == specific_date_true['start_date']
    # delete created employee
    r = client.delete(f'{EmployeeApi_URL}/{empl_id}')
    assert r.status_code == 204
