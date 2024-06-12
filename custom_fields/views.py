from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import CustomField
from .serializers import CustomFieldSerializer
from rest_framework.permissions import AllowAny
from simplecrm.models import CustomUser


@api_view(['POST'])
@permission_classes([AllowAny]) 
def create_custom_field(request):
    if request.method == 'POST':
        # Extract data from the request
        model_name = request.data.get('model_name')
        name = request.data.get('name')
        value = request.data.get('value')
        field_type = request.data.get('field_type')
        user = request.user  # Assuming user authentication is used
        tenant = user.tenant  # Assuming tenant is associated with the user
        
        # Validate the data
        if not model_name or not name or not field_type:
            return Response({'error': 'Missing required data'}, status=400)
        
        # Save the data to the database
        custom_field_data = {
            'model_name': model_name,
            'name': name,
            'value': value,
            'field_type': field_type,
            'user': user.id,
            'tenant': tenant.id
        }
        
        serializer = CustomFieldSerializer(data=custom_field_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
