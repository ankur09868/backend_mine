# views.py

from django.http import JsonResponse
from django.views import View
class TrackOpenCountView(View):
    def get(self, request, *args, **kwargs):
        global count
        return JsonResponse({'total_count': count})
