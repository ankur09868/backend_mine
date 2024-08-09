import os
import sys
import django
from datetime import datetime, timedelta
from django.core.management import call_command
import schedule
import time

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def generate_daily_report():
    call_command('generate_daily_report')

# Schedule daily report generation at midnight
schedule.every().day.at("00:00").do(generate_daily_report)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
