# this script populates database using api and json data

import json
import requests
import os

basedir = os.path.abspath(os.path.dirname(__file__))
baseurl = 'http://127.0.0.1:5000'

if __name__ == '__main__':
    with open(basedir, 'employees.txt') as json_file:
        data = json.load(json_file)
        for empl in data:
            response = requests.post(baseurl + '/api/employees', empl)
            print('\nAdded: \n')
            print(response.json())
        print('\nEMPLOYEES dataset after series of POST requests: \n')
        response = requests.get(baseurl + '/api/employees')
        print(response.json())


