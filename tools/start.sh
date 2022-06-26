#! /bin/bash

cd /home/igor/prj/python/ya-sch/
echo $(date) start >> enrollment/t
source venv/bin/activate
cd enrollment
echo $(date) point 2 >> t
python . &>>log.log
echo $(date) point 3 >> t
