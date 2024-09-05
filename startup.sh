#!/bin/bash

# Navigate to the application directory
cd /home/site/wwwroot

# Create and activate the virtual environment
python -m venv antenv
source antenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Django application
python manage.py runserver 0.0.0.0:8000
