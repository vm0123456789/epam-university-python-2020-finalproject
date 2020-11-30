# this script populates database using api and json data

import json
import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))
baseurl = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    # populate db with departments.txt dataset
    with open(basedir, 'departments.txt') as json_file:
        data = json.load(json_file)
        for department in data:
            response = requests.post(baseurl + '/api/departments', department)
            print('\nAdded: \n')
            print(response.json)
        print('\nDEPARTMENTS dataset after series of POST requests: \n')
        response = requests.get(baseurl, '/api/departments')
        print(response.json())

    with open(basedir, 'employees.txt') as json_file:
        # populate db with employees.txt datatset
        data = json.load(json_file)
        for empl in data:
            response = requests.post(baseurl + '/api/employees', empl)
            print('\nAdded: \n')
            print(response.json())
        print('\nEMPLOYEES dataset after series of POST requests: \n')
        response = requests.get(baseurl + '/api/employees')
        print(response.json())


