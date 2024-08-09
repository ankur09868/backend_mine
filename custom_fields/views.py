from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import CustomField
from .serializers import CustomFieldSerializer
from rest_framework.permissions import AllowAny
# from simplecrm.models import CustomUser
from django.conf import settings
from simplecrm.models import CustomUser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from accounts.models import Account
from contacts.models import Contact
from leads.models import Lead
from documents.models import Document
from interaction.models import Interaction, calls
from tenant.models import Tenant

MODEL_CLASSES = {
    'account': Account,
    'call':calls,
    'contact':Contact,
    'interaction':Interaction,
    'lead': Lead,
    'document':Document,
}



@api_view(['POST'])
@permission_classes([AllowAny]) 
def create_custom_field(request):
    if request.method == 'POST':
        # Extract data from the request
        model_name = request.data.get('model_name')
        custom_field = request.data.get('custom_field')
        value = request.data.get('value')
        field_type = request.data.get('field_type')
        user_id = request.data.get('user_id') 
        tenant = request.data.get('tenant')  

        if not model_name or not custom_field or not field_type or not user_id or not tenant:
            return Response({'error': 'Missing required data'}, status=400)
    
        custom_field_data = {
            'model_name': model_name,
            'custom_field': custom_field,
            'value': value,
            'field_type': field_type,
            'user': user_id,  
            'tenant': Tenant
        }
        serializer = CustomFieldSerializer(data=custom_field_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

def retrieve_custom_fields(request, model_name, entity_id):
    try:
        if model_name not in ['account', 'lead', 'interaction', 'calls', 'contact']:
            return JsonResponse({'error': 'Invalid model name'}, status=400)

        entity = get_object_or_404(MODEL_CLASSES[model_name], id=entity_id)

        custom_fields = CustomField.objects.filter(model_name=model_name)

        custom_fields_data = []
        for field in custom_fields:
           
            value = field.value if field.entity_id == entity_id else None

            custom_fields_data.append({
                'custom_field': field.custom_field,
                'value': value,
                'field_type': field.field_type
            })

        
        data = {
            'entity': {
                'id': entity.id,
                'name': str(entity),
            },
            'custom_fields': custom_fields_data
        }

       
        if hasattr(entity, 'email'):
            data['entity']['email'] = entity.email

        return JsonResponse(data)

    except (Account.DoesNotExist, Lead.DoesNotExist, Interaction.DoesNotExist, calls.DoesNotExist, Contact.DoesNotExist):
        return JsonResponse({'error': f'{model_name.capitalize()} with ID {entity_id} not found'}, status=404)
    except CustomField.DoesNotExist:
        return JsonResponse({'error': 'Custom fields not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
