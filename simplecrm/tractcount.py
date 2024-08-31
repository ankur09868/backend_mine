# views.py

from django.http import JsonResponse
from django.views import View
from interaction.models import Email
from django.db.models import Sum  
class TrackOpenCountView(View):
    def get(self, request, *args, **kwargs):
        # Calculate the total number of opens across all emails
        total_count = Email.objects.aggregate(total_opens=Sum('open_count'))['total_opens'] or 0
        
        return JsonResponse({'total_count': total_count})
