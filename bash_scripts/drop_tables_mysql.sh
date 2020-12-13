#!/bin/bash

# run under root
# if `foreign key constraint` run 2 times

mysql -Nse 'show tables' departments_app | while read table; do mysql -e "drop table $table" departments_app; done