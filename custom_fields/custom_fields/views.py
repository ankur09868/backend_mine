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
from calls.models import calls
from contacts.models import Contact
from leads.models import Lead
from documents.models import Document
from interaction.models import Interaction
from product.models import Product
from vendors.models import Vendors
from tenant.models import Tenant
from django.contrib.contenttypes.models import ContentType

MODEL_CLASSES = {
    'account': Account,
    'call':calls,
    'contact':Contact,
    'interaction':Interaction,
    'lead': Lead,
    'document':Document,
    'product':Product,
    'vendors':Vendors,
}

@api_view(['POST'])
@permission_classes([AllowAny])
def create_custom_field(request):
    if request.method == 'POST':
        # Extract data from the request
        model_name = request.data.get('model_name')
        custom_field_name = request.data.get('custom_field')
        value = request.data.get('value')
        field_type = request.data.get('field_type')
        tenant_id = request.headers.get('X-Tenant-ID')
        object_id = request.data.get('object_id')

        if not model_name or not custom_field_name or not field_type or not tenant_id:
            return Response({'error': 'Missing required data'}, status=400)

        try:
            # Get the ContentType for the model
            content_type = ContentType.objects.get(model=model_name.lower())
        except ContentType.DoesNotExist:
            return Response({'error': 'Invalid model name'}, status=400)

        custom_field_data = {
            'model_name': model_name,
            'custom_field': custom_field_name,
            'value': value,
            'field_type': field_type,
            'tenant': tenant_id,
            'content_type': content_type.id,
            'object_id': object_id # You may need to handle this dynamically
        }

        serializer = CustomFieldSerializer(data=custom_field_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

@api_view(['GET'])
def retrieve_custom_fields(request, model_name, entity_id):
    try:
        # Check if the model name is valid
        if model_name not in MODEL_CLASSES:
            return Response({'error': 'Invalid model name'}, status=400)

        # Retrieve the entity instance
        entity = get_object_or_404(MODEL_CLASSES[model_name], id=entity_id)

        # Get the ContentType for the model
        content_type = ContentType.objects.get_for_model(entity)

        # Filter custom fields for the given model name and entity
        custom_fields = CustomField.objects.filter(
            content_type=content_type,
            object_id=entity_id
        )

        # Prepare the data for custom fields
        custom_fields_data = []
        for field in custom_fields:
            custom_fields_data.append({
                'custom_field': field.custom_field,
                'value': field.value,
                'field_type': field.field_type
            })

        # Prepare the response data
        data = {
            'entity': {
                'id': entity.id,
                'name': str(entity),
            },
            'custom_fields': custom_fields_data
        }

        # Include email if it exists on the entity
        if hasattr(entity, 'email'):
            data['entity']['email'] = entity.email

        return Response(data)

    except MODEL_CLASSES[model_name].DoesNotExist:
        return Response({'error': f'{model_name.capitalize()} with ID {entity_id} not found'}, status=404)
    except ContentType.DoesNotExist:
        return Response({'error': 'Invalid model name'}, status=400)
    except CustomField.DoesNotExist:
        return Response({'error': 'Custom fields not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def retrieve_all_custom_fields(request):
    try:
        # Retrieve all custom fields
        custom_fields = CustomField.objects.all()

        # Prepare the data for custom fields
        custom_fields_data = []
        for field in custom_fields:
            custom_fields_data.append({
                'model_name': field.model_name,
                'entity_id': field.entity_id,
                'custom_field': field.custom_field,
                'value': field.value,
                'field_type': field.field_type
            })

        # Prepare the response data
        data = {
            'custom_fields': custom_fields_data
        }

        return Response(data)

    except CustomField.DoesNotExist:
        return Response({'error': 'Custom fields not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
