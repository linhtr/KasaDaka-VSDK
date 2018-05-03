#!/bin/bash
# initilizes the project on the heroku environment
python3 manage.py makemigrations service_development #make migrations
python3 manage.py migrate #perform migrations
python3 manage.py loaddata initial_data.json #import database data
python3 manage.py createsuperuser #create admin
