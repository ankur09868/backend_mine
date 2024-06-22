from django.shortcuts import render
from leads.models import Lead
from django.db.models import Sum
from opportunities.models import Opportunity
from .models import Report
from django.http import JsonResponse
# Create your views here.

def generate_report():

    closed_won_revenue = Opportunity.objects.filter(stage__status='CLOSED WON').aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    other_lead_amount = Lead.objects.exclude(stage__status='closed won').aggregate(total_amount=Sum('opportunity_amount'))['total_amount'] or 0

 
    total_leads = Lead.objects.count()

    report = Report(
        leads_amount=other_lead_amount,
        revenue=closed_won_revenue,
        total_leads=total_leads,
    )
    report.save()

    return report

def generate_and_get_report_view(request):
    report = generate_report()

    # Prepare the data for the latest report
    data = {
        'created_at': report.created_at,
        'leads_amount': report.leads_amount,
        'revenue': report.revenue,
        'total_leads': report.total_leads,
    }

    return JsonResponse(data)