from rest_framework import generics
from .models import meetings
from .serializers import meetingsSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
class MeetingListCreateAPIView(ListCreateAPIView):
    queryset = meetings.objects.all()
    serializer_class = meetingsSerializer

class MeetingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = meetings.objects.all()
    serializer_class = meetingsSerializer
