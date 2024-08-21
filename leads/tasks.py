from celery import shared_task
from datetime import date, timedelta
from django.db.models import Sum
from .models import Report, Lead
from opportunities.models import Opportunity

# Function to get today's date
def get_today():
    return date.today()

# Function to get yesterday's date
def get_yesterday():
    return date.today() - timedelta(days=1)

@shared_task
def generate_or_get_report():
    today = get_today()
    yesterday = get_yesterday()
   
    report_today = Report.objects.filter(created_at__date=today).first()
    
    if report_today:
        return report_today
    
    report_yesterday = Report.objects.filter(created_at__date=yesterday).first()
    
    if report_yesterday:
        closed_won_revenue = Opportunity.objects.filter(stage__status='CLOSED WON').aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0
        other_lead_amount = Lead.objects.exclude(stage__status='closed won').aggregate(total_amount=Sum('opportunity_amount'))['total_amount'] or 0
        total_leads = Lead.objects.count()

        new_report = Report(
            leads_amount=other_lead_amount,
            revenue=closed_won_revenue,
            total_leads=total_leads,
            created_at=today
        )
        new_report.save()
        
        return new_report
    else:
        return None

def get_yesterday_report():
    yesterday = get_yesterday()
    report_yesterday = Report.objects.filter(created_at__date=yesterday).first()
    return report_yesterday

def get_today_report():
    today = get_today()
    report_today = Report.objects.filter(created_at__date=today).first()
    return report_today
