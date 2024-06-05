from django.db.models import Count, Max, Sum
from datetime import timedelta
from django.utils import timezone
from .models import Opportunity

def calculate_rfm_metrics(customer):
    latest_opportunity_date = customer.opportunities.aggregate(latest_date=Max('closedOn'))['latest_date']
    if latest_opportunity_date:
        recency = (timezone.now() - latest_opportunity_date).days
    else:
        recency = -1

    frequency = customer.opportunities.count()

    monetary = customer.opportunities.aggregate(total_amount=Sum('amount'))['total_amount']

    return recency, frequency, monetary
