#!/bin/bash

# create migrations for main db and test db

# ----------------------------------------------
export FLASK_APP=departments_app.py

if [ ! -d /migrations/main_migrations ]; then
  flask db init -d migrations/main_migrations
  flask db migrate -d migrations/main_migrations
  flask db upgrade -d migrations/main_migrations
else
  flask db migrate -d migrations/main_migrations
  flask db upgrade -d migrations/main_migrations
fi

echo Main migration done!!!

#-----------------------------------------------

export FLASK_APP=departments_test_app.py

if [ ! -d /migrations/test_migrations ]; then
  flask db init -d migrations/test_migrations
  flask db migrate -d migrations/test_migrations
  flask db upgrade -d migrations/test_migrations
else
  flask db migrate -d migrations/test_migrations
  flask db upgrade -d migrations/test_migrations
fi

echo Test migration done!!!