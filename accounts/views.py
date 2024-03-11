from django.shortcuts import render
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
# Create your views here.

from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Account

def delete_all_accounts():
    try:
        # Delete all entries of the Account model
        Account.objects.all().delete()
        print("All accounts deleted successfully.")
    except Exception as e:
        print(f"Error occurred while deleting accounts: {str(e)}")

# Call the function to delete all accounts

class AccountListAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  # Allowing any user to access this view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a default user if it doesn't exist
        self.default_user = self.create_default_user()

    def create_default_user(self):
        # Check if the default user already exists
        default_user, created = User.objects.get_or_create(
            username='dmfnv ndkfj v',
            email='john@example.com'
        )
        if created:
            default_user.set_password('password123')
            default_user.save()
        return default_user

    def perform_create(self, serializer):
        # Assign the default user to createdBy field of the account
        serializer.save(createdBy=self.default_user)

    def post(self, request, *args, **kwargs):
        try:
            # Call the base class post() method to handle the POST request
            return super().post(request, *args, **kwargs)
        except Exception as e:
            # Log the error and return an error response
            print(f"Error occurred while handling POST request: {str(e)}")
            return Response({"error": "Failed to create account."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)