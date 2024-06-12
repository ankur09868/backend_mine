from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import CustomField
from .serializers import CustomFieldSerializer
from rest_framework.permissions import AllowAny
# from simplecrm.models import CustomUser
from django.conf import settings
from simplecrm.models import CustomUser
# US = settings.AUTH_USER_MODEL




@api_view(['POST'])
@permission_classes([AllowAny]) 
def create_custom_field(request):
    if request.method == 'POST':
        # Extract data from the request
        model_name = request.data.get('model_name')
        custom_field = request.data.get('custom_field')
        value = request.data.get('value')
        field_type = request.data.get('field_type')
        user_id = request.data.get('user_id')  # Assuming you pass the user ID in the request payload
        tenant_id = request.data.get('tenant_id')  # Assuming you pass the tenant ID in the request payload
        
        # Validate the data
        if not model_name or not custom_field or not field_type or not user_id or not tenant_id:
            return Response({'error': 'Missing required data'}, status=400)
        
        # You can perform additional validation here, such as checking if the user and tenant exist
        
        # Save the data to the database
        custom_field_data = {
            'model_name': model_name,
            'custom_field': custom_field,
            'value': value,
            'field_type': field_type,
            'user_id': user_id,  # Assign the user ID to the custom field data
            'tenant_id': tenant_id,  # Assign the tenant ID to the custom field data
        }
        serializer = CustomFieldSerializer(data=custom_field_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
