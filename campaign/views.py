# campaign/views.py

from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
class CampaignViewSet(ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    
class CampaignDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = (AllowAny,) 