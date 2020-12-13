#!/bin/bash

flask run &

sleep 1

python ./app/tests/test_data/post_from_json.py

kill $!

