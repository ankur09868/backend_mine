from django.core.management.base import BaseCommand
from datetime import date
from leads.models import Lead
from django.db.models import Sum
from opportunities.models import Opportunity
from reports.models import Report

class Command(BaseCommand):
    help = 'Generates daily report'

    def handle(self, *args, **options):
        today = date.today()

        # Check if a report for today already exists
        report_today = Report.objects.filter(created_at=today).first()

        if report_today:
            self.stdout.write(self.style.WARNING(f'Report for {today} already exists. Skipping generation.'))
            return

        # Calculate necessary data for the report
        closed_won_revenue = Opportunity.objects.filter(stage__status='CLOSED WON').aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0
        other_lead_amount = Lead.objects.exclude(stage__status='closed won').aggregate(total_amount=Sum('opportunity_amount'))['total_amount'] or 0
        total_leads = Lead.objects.count()

        # Create a new report object for today
        new_report = Report(
            leads_amount=other_lead_amount,
            revenue=closed_won_revenue,
            total_leads=total_leads,
            created_at=today
        )
        new_report.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully generated report for {today}'))
