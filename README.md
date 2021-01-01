# EPAM University RD External Python Course Graduation Work

Prepared by _Viktor Mishyn_

==============================

## Description

Simple web application for managing departments and employees.  
The application uses RESTful API for storing data and reading from a database.

The web application should allow:

* display a list of departments, and the average salary (calculated automatically) for these departments,
* display a list of employees in the departments with an indication of the salary for each employee and a search field
  to search for employees born on a certain date or in the period between dates,
* change (add / edit / delete) the above data

The web application is built using Flask Python framework along with Bootstrap CSS framework and jQuery JS library.  
The RESTful API is built using Flask and MySQL database.

## Deployment

1. OS: The server should be deployed on GNU/Linux OS (e.g. Ubuntu 20.04).
2. DB: Before the deployment we should create and configure MySQL db server, using cli commands from './notes.txt'.
  Database URI specified in './.flaskenv' file.
3. Also it is needed to have installed Python 3.8+, pip, venv and libmysqlclient-dev:
  ```bash
  sudo apt install python3
  sudo apt install python3-pip
  sudo apt install python3-venv
  sudo apt install libmysqlclient-dev
  ```
4. On GNU/Linux OS with installed and configured MySQL server we can deploy application server using './init.sh' script.
  It will create and activate a python virtual environment, create migrations, populate our database with mockup data
  and run Gunicorn WSGI HTTP server

## API endpoints

* '/api/employees'
    * GET - get all employees
    * POST - create new employee. Data (every field required):
      ```json
      {'name': <str>, 'birthday': <'%Y-%m-%d' str>, 'salary': <int>, 'dep_name': <str>}
      ````
* '/api/employees/<empl_id>'
    * GET - get employee by id
    * PUT - update employee information. Data (any field):
      ```json 
      {'name': <str>, 'birthday': <'%Y-%m-%d' str>, 'salary': <int>, 'dep_name': <str>}
      ````
    * DELETE - delete employee by id  
    
    
* '/api/departments'
    * GET - get all departments. The function uses '/api/departments/<dep_id>' to collect departments data.
    * POST - create new department. Data:
      ```json 
      {'name': <str>}
      ````
    
* '/api/departments/<dep_id>'
    * GET - get department by id. Returns json with department id, department name, list of employees and average
      salary.
    * PUT - update department information. Data:
      ```json 
      {'name': <str>}
      ````
    * DELETE - delete department with all its employees (!!!)  
    

* '/api/search'
    * GET - get employees by birthday date / period of dates. Data:
      ```json 
      {'start_date': <'%Y-%m-%d' str>, 'end_date': <'%Y-%m-%d' str>}
      ```  

* '/api/search/<dep_id>'
    * GET - get employees of the department by birthday date / period of dates. Data:
      ```json 
      {'start_date': <'%Y-%m-%d' str>, 'end_date': <'%Y-%m-%d' str>}
      ```  



