from django.db import connections
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from .models import Tenant  # Ensure this is the correct path to your Tenant model
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware(MiddlewareMixin):
    current_tenant_id = None

    def process_request(self, request):
        logger.debug("Processing request in TenantMiddleware")
        if request.path.startswith('/login/') or request.path.startswith('/register/') or request.path.startswith('/createTenant/'):
            logger.debug("Skipping tenant processing for login or register endpoint")
            return

        tenant_id = request.headers.get('X-Tenant-Id')
        logger.debug(f"Received Tenant ID: {tenant_id}")

        if not tenant_id:
            logger.error("No Tenant ID found in headers")
            return HttpResponse('No Tenant ID provided', status=400)
        
        if TenantMiddleware.current_tenant_id == tenant_id:
            logger.debug(f"Tenant ID {tenant_id} already connected. Skipping reconnection.")
            return

        # Retrieve tenant's username and password from database
        try:
            tenant = Tenant.objects.get(id=tenant_id)  # Use the 'id' field for tenant_id
            tenant_username = tenant.db_user
            tenant_password = tenant.db_user_password
            logger.debug(f"Tenant found: {tenant}")
        except Tenant.DoesNotExist:
            # Handle case where tenant does not exist
            logger.error(f"Tenant does not exist for Tenant ID: {tenant_id}")
            return HttpResponse('Tenant does not exist', status=404)
        
        # Set the database connection settings for the tenant
        connection = connections['default']
        connection.settings_dict['USER'] = tenant_username
        connection.settings_dict['PASSWORD'] = tenant_password
        logger.debug(f"Set database user to: {tenant_username}")

        # Ensure the connection is re-established
        connection.close()
        connection.connect()
        logger.debug("Database connection re-established")

        # Update the current tenant ID
        TenantMiddleware.current_tenant_id = tenant_id
