from django.shortcuts import render
from rest_framework import generics
from .models import meetings  # Assuming the model name is Meeting based on the provided serializer
from .serializers import meetingsSerializer  # Importing the MeetingSerializer instead of LeadSerializer
from rest_framework.permissions import IsAdminUser

class MeetingListAPIView(generics.ListCreateAPIView):
    queryset = meetings.objects.all()  # Using Meeting model queryset instead of Lead
    serializer_class = meetingsSerializer  # Using MeetingSerializer instead of LeadSerializer
    # permission_classes = (IsAdminUser,)  # Optionally, uncomment and modify the permission classes

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")
            raise  # Re-raise the exception for Django to handle
