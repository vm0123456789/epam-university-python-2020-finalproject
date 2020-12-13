#!/bin/bash

flask run &

python ./app/tests/test_data/post_from_json.py

kill $!

