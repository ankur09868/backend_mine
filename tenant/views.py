import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Tenant
from .serializers import TenantSerializer
from django.db import connection
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.conf import settings
from simplecrm import database_settings
@csrf_exempt
def create_tenant_role(tenant_id, password):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"create role crm_tenant_{tenant_id} with inherit login password '{password}' in role crm_tenant;")
        
        # Dynamically update DATABASES settings only if role creation is successful
        database_settings = settings.get_database_settings(tenant_id, password)
        settings.DATABASES['default'] = database_settings

        return True
    except Exception as e:
        print(f"Error creating tenant role: {e}")
        return False

@csrf_exempt
def tenant_list(request):
    """
    View to retrieve a list of all tenants or create a new tenant.
    """
    if request.method == 'GET':
        tenants = Tenant.objects.all()
        serializer = TenantSerializer(tenants, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        tenant_id = data.get('tenant_id')
        db_user_password = data.get('password')
        
        try:
            # Start a database transaction
            with connection.cursor() as cursor:
                cursor.execute("BEGIN")
                
                # Create the tenant in the database
                tenant = Tenant.objects.create(id=tenant_id, db_user=f"crm_tenant_{tenant_id}", db_user_password=db_user_password)
                
                # Create role for the tenant
                cursor.execute(f"CREATE ROLE crm_tenant_{tenant_id} INHERIT LOGIN PASSWORD '{db_user_password}' IN ROLE crm_tenant")

                # Commit the transaction
                cursor.execute("COMMIT")
                
                return JsonResponse({'msg': 'Tenant registered successfully'})
        except IntegrityError as e:
            # Rollback the transaction if any error occurs
            cursor.execute("ROLLBACK")
            return JsonResponse({'msg': f'Error creating tenant: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'msg': f'Error creating tenant: {str(e)}'}, status=500)
    
    else:
        return JsonResponse({'msg': 'Method not allowed'}, status=405)

@csrf_exempt
def tenant_detail(request, tenant_id):
    """
    View to retrieve details of a specific tenant by ID.
    """
    if request.method == 'GET':
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            serializer = TenantSerializer(tenant)
            return JsonResponse(serializer.data)
        except Tenant.DoesNotExist:
            return JsonResponse({'msg': 'Tenant not found'}, status=404)
    else:
        return JsonResponse({'msg': 'Method not allowed'}, status=405)
