#!/bin/bash
source /home/site/wwwroot/antenv/bin/activate
exec gunicorn --bind 0.0.0.0:8000 simplecrm.wsgi:application
