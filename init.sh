#!/bin/bash

# before running this script make sure that you have properly configured MySQL 'departments_app' database

echo ""
echo "Creating virtual environment..."
echo ""
sleep 1
python3 -m venv env

echo "================================================================="
echo ""
echo "Activating virtual environment..."
echo ""
sleep 1
source env/bin/activate

echo "================================================================="
echo ""
echo "Installing dependencies..."
echo ""
sleep 1
pip install wheel
pip install -r requirements.txt

echo "================================================================="
echo ""
echo "Creating migrations..."
echo ""
sleep 1
./bash_scripts/migrations.sh

echo "================================================================="
echo ""
echo "Populating database with mockup data..."
echo ""
sleep 1
./bash_scripts/populate_db.sh

echo "================================================================="
echo ""
echo "Running gunicorn..."
echo ""
sleep 1
gunicorn -w 4 -b 127.0.0.1:5000 departments_app:app --access-logfile logs/departments_app_Gunicorn.log