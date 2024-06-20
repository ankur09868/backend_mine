from django.shortcuts import render
from rest_framework import generics
from .models import Lead
from django.http import HttpResponse
from .serializers import LeadSerializer
from rest_framework.permissions import AllowAny  # Import AllowAny
from django.http import JsonResponse
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.decorators.http import require_http_methods
from stage.models import Stage  # Import your Stage model here

class LeadListCreateAPIView(ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (AllowAny,)  # Use AllowAny permission

class LeadDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (AllowAny,)  # Use AllowAny permission


#stage for lead

@require_http_methods(["GET"])
def lead_stage(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        if lead.stage_id:
            stage = Stage.objects.get(id=lead.stage_id, model_name='lead')  # Assuming model_name field exists in Stage
            stage_data = {
                'id': stage.id,
                'status': stage.status,
                'model_name': stage.model_name,
            }
            return JsonResponse(stage_data, status=200)
        else:
            return JsonResponse({'error': 'Lead stage not found'}, status=404)
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead not found'}, status=404)
    except Stage.DoesNotExist:
        return JsonResponse({'error': 'Stage not found for this lead'}, status=404)


# @require_http_methods(["GET"])
# def all_stages(request):
#     try:
#         stages = Stage.objects.filter(model_name='lead')  # Adjust the filter as per your model

#         if stages.exists():
#             stages_data = [{
#                 'id': stage.id,
#                 'status': stage.status,
#             } for stage in stages]
#             return JsonResponse({'stages': stages_data}, status=200)
#         else:
#             return JsonResponse({'error': 'No stages found'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def all_stages(request):
    tenant_id = request.headers.get('X-Tenant-ID')
    if not tenant_id:
        return JsonResponse({'error': 'Tenant ID is required in headers'}, status=400)

    try:
        stages = Stage.objects.filter(model_name='lead', tenant_id=tenant_id)  # Adjust the filter as per your model

        if stages.exists():
            stages_data = [{
                'id': stage.id,
                'status': stage.status,
            } for stage in stages]
            return JsonResponse({'stages': stages_data}, status=200)
        else:
            return JsonResponse({'error': 'No stages found for the given tenant'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




