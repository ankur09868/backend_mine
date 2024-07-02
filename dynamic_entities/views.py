from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import DynamicModel, DynamicField
from .serializers import DynamicModelSerializer
from django.db import models, connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
import sys
import re

User =  get_user_model()


def get_dynamic_model_class(model_name):
    """Get the dynamic model class."""
    class Meta:
        app_label = 'dynamic_entities'
    attrs = {'__module__': 'dynamic_entities.models', 'Meta': Meta}
    fields = DynamicField.objects.filter(dynamic_model__model_name=model_name)
    for field in fields:
        field_type = field.field_type
        if field_type == 'string':
            attrs[field.field_name] = models.CharField(max_length=255)
        elif field_type == 'integer':
            attrs[field.field_name] = models.IntegerField()
        elif field_type == 'text':
            attrs[field.field_name] = models.TextField()
        elif field_type == 'boolean':
            attrs[field.field_name] = models.BooleanField()
        elif field_type == 'date':
            attrs[field.field_name] = models.DateField()
        else:
            raise ValueError(f'Unknown field type: {field_type}')
    return type(model_name, (models.Model,), attrs)


def deregister_dynamic_model(model_name):
    """Deregister the dynamic model class."""
    model_module = sys.modules.get('dynamic_entities.models')
    if model_module:
        lowercase_model_name = model_name.lower()
        capitalized_model_name = model_name.capitalize()
        if hasattr(model_module, lowercase_model_name):
            delattr(model_module, lowercase_model_name)
        if hasattr(model_module, capitalized_model_name):
            delattr(model_module, capitalized_model_name)

@method_decorator(csrf_exempt, name='dispatch')
class CreateDynamicModelView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = DynamicModelSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            model_name = validated_data.get('model_name')
            fields = validated_data.get('fields')

            try:
                field_definitions = {
                     '__module__': 'dynamic_entities.models', 
                    'Meta': type('Meta', (), {'app_label': 'dynamic_entities'})
                }
                for field in fields:
                    field_name = field['field_name']
                    field_type = field['field_type']
                    if field_type == 'string':
                        field_definitions[field_name] = models.CharField(max_length=255)
                    elif field_type == 'integer':
                        field_definitions[field_name] = models.IntegerField()
                    elif field_type == 'text':
                        field_definitions[field_name] = models.TextField()
                    elif field_type == 'boolean':
                        field_definitions[field_name] = models.BooleanField()
                    elif field_type == 'date':
                        field_definitions[field_name] = models.DateField()
                    else:
                        return Response({'success': False, 'message': f'Unknown field type: {field_type}'}, status=status.HTTP_400_BAD_REQUEST)

                model_class = type(model_name, (models.Model,), field_definitions)
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model_class)

                default_user = request.user if request.user.is_authenticated else User.objects.first()
                if not default_user:
                    return Response({'success': False, 'message': 'No default user found'}, status=status.HTTP_400_BAD_REQUEST)
                
                dynamic_model = DynamicModel.objects.create(model_name=model_name, created_by=default_user)


                for field in fields:
                    DynamicField.objects.create(dynamic_model=dynamic_model, field_name=field['field_name'], field_type=field['field_type'])
                
                table_name = f"dynamic_entities_{model_name.lower()}"
                with connection.cursor() as cursor:
                    cursor.execute(f'ALTER TABLE "{table_name}" OWNER TO crm_tenant')
                    cursor.execute(f'GRANT ALL PRIVILEGES ON TABLE "{table_name}" TO crm_tenant')
                    cursor.execute(f'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "{table_name}" TO public')


                return Response({'success': True, 'message': f'Dynamic model "{model_name}" created successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class DynamicModelListView(APIView):
    def get(self, request, *args, **kwargs):
        dynamic_models = DynamicModel.objects.all()
        response_data = []

        for dynamic_model in dynamic_models:
            try:
              
                # Sanitize the model name to ensure it's a valid SQL identifier
                model_name = dynamic_model.model_name.lower()
                sanitized_model_name = re.sub(r'\W|^(?=\d)', '_', model_name)
                table_name = f"dynamic_entities_{sanitized_model_name}"

                # Check if the table exists
                with connection.cursor() as cursor:
                    cursor.execute("SELECT to_regclass(%s)", [table_name])
                    if cursor.fetchone()[0] is None:
                        raise ValueError(f"Table for model {dynamic_model.model_name} does not exist.")

                fields = DynamicField.objects.filter(dynamic_model=dynamic_model)
                fields_data = [{'field_name': field.field_name, 'field_type': field.field_type} for field in fields]

                model_data = {
                    'model_name': dynamic_model.model_name,
                    'created_by': dynamic_model.created_by.username,
                    'tenant': dynamic_model.tenant.name if dynamic_model.tenant else None,
                    'fields': fields_data
                }
                response_data.append(model_data)
            except ValueError:
                dynamic_model.delete()
                DynamicField.objects.filter(dynamic_model=dynamic_model).delete()


        return Response(response_data, status=status.HTTP_200_OK)



class DynamicModelDataView(APIView):
    def get(self, request, model_name, *args, **kwargs):
        try:
            model_class = get_dynamic_model_class(model_name)
            data = model_class.objects.all().values()
            return Response(list(data), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, model_name, *args, **kwargs):
        try:
            model_class = get_dynamic_model_class(model_name)
            data = request.data
            instance = model_class.objects.create(**data)
            return Response({'success': True, 'message': 'Data added successfully', 'data': instance.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, model_name, *args, **kwargs):
        try:
            model_class = get_dynamic_model_class(model_name)
            data = request.data
            instance_id = data.pop('id', None)
            if not instance_id:
                return Response({'success': False, 'message': 'ID is required for updating data'}, status=status.HTTP_400_BAD_REQUEST)
            instance = model_class.objects.filter(id=instance_id).update(**data)
            return Response({'success': True, 'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

class DeleteDynamicModelView(APIView):
    def delete(self, request, model_name, *args, **kwargs):
        try:
            model_class = get_dynamic_model_class(model_name)
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(model_class)

            deregister_dynamic_model(model_name)
            DynamicModel.objects.filter(model_name=model_name).delete()
            DynamicField.objects.filter(dynamic_model__model_name=model_name).delete()
            return Response({'success': True, 'message': f'Model {model_name} deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

