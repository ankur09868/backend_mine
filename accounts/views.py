from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import AllowAny
# from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from simplecrm.models import CustomUser
# from tenant.models import Tenant
# from django.http import JsonResponse

class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)
   

class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  # Allowing any user to access this view


# def retrieve_accounts_by_tenant_id(request, tenant_id):
#     try:
#         # Retrieve the tenant object
#         tenant = Tenant.objects.get(id=tenant_id)
#         # Fetch all accounts belonging to the given tenant
#         accounts = Account.objects.filter(tenant=tenant)
#         # Serialize the accounts
#         serialized_accounts = []
#         for account in accounts:
#             if account.dynamic_fields:  # Check if dynamic_fields is not empty
#                 serialized_account = {
#                     'id': account.id,
#                     'Name': account.Name,
#                     'dynamic_fields': account.dynamic_fields,
#                     # Include other fields as needed
#                 }
#                 serialized_accounts.append(serialized_account)
#         return JsonResponse(serialized_accounts, safe=False)
#     except Tenant.DoesNotExist:
#         # Handle Tenant not found
#         return JsonResponse({'error': 'Tenant not found'}, status=404)














     # def get_queryset(self):
    #     # Filter queryset based on user's tenant
    #     user_tenant = self.request.user.tenant
    #     return Account.objects.filter(tenant=user_tenant)

    # def perform_create(self, serializer):
    #     # Set the tenant of the account before saving
    #     serializer.save(tenant=self.request.user.tenant)

