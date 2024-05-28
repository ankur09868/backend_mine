from django.shortcuts import render
from rest_framework import generics
from .models import calls  # Assuming the model name is call based on the provided serializer
from .serializers import callsSerializer  # Importing the callSerializer instead of LeadSerializer
from rest_framework.permissions import IsAdminUser

class callsListAPIView(generics.ListCreateAPIView):
    queryset = calls.objects.all()  # Using call model queryset instead of Lead
    serializer_class = callsSerializer  # Using callSerializer instead of LeadSerializer
    # permission_classes = (IsAdminUser,)  # Optionally, uncomment and modify the permission classes

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")
            raise  # Re-raise the exception for Django to handle

class callsDetailAPIView(generics.RetrieveAPIView):
    queryset = calls.objects.all()
    serializer_class = callsSerializer
    # Uncomment the line below to restrict access to admin users only
    # permission_classes = (IsAdminUser,)
