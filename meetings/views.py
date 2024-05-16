from django.shortcuts import render
from rest_framework import generics
from .models import meetings  # Assuming the model name is Meeting based on the provided serializer
from .serializers import meetingsSerializer  # Importing the MeetingSerializer instead of LeadSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated

class MeetingListAPIView(generics.ListCreateAPIView):
    serializer_class = meetingsSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        """
        This view should return a list of all the meetings
        for the tenant of the currently authenticated user.
        """
        user = self.request.user
        return meetings.objects.filter(tenant=user.tenant)

    def perform_create(self, serializer):
        """
        Save the new meeting with the tenant of the currently authenticated user.
        """
        serializer.save(tenant=self.request.user.tenant)