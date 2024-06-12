
from django.apps import apps
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import deduplicate_model

@api_view(['POST'])
def deduplicate_view(request):
    app_name = request.data.get('app_name')
    model_name = request.data.get('model')
    unique_field = request.data.get('field')
    
    if not app_name or not model_name or not unique_field :
        return JsonResponse({'status': 'error', 'message': 'App-Name,Model name and field name are required.'}, status=400)
    
    try:
        model_class = apps.get_model(app_name, model_name)
    except LookupError:
        return JsonResponse({'status': 'error', 'message': f'Model {model_name} not found in App.'}, status=400)

    try:
        deduplicate_model(model_class, unique_field)
        return JsonResponse({'status': 'success', 'message': f'Duplicates removed successfully from {model_name}.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
