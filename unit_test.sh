#! /bin/bash

python . &
sleep 1
python unit_test.py "http://localhost:8080"
status_code=$?
kill $!
exit $status_code
