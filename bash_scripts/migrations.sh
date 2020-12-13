#!/bin/bash

if [ ! -d /migrations ]; then
  flask db init
  flask db migrate
  flask db upgrade
else
  flask db migrate
  flask db upgrade
fi

echo Migration done!!!