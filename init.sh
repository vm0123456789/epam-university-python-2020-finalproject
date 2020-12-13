#!/bin/bash

# before running this script make sure that you have properly configured MySQL 'departments_app' database

python3 -m venv env

source env/bin/activate

pip install wheel

pip install -r requirements.txt

./bash_scripts/migrations.sh

./bash_scripts/populate_db.sh

flask run
