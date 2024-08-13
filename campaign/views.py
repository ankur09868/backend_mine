# campaign/views.py

from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from .models import InstagramCampaign
from .models import WhatsAppCampaign
from .models import EmailCampaign
from .serializers import EmailCampaignSerializer
from .serializers import WhatsAppCampaignSerializer
from .serializers import InstagramCampaignSerializer
from rest_framework import status
class CampaignViewSet(ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    
class CampaignDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the campaign instance
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Prepare the response data
        response_data = {
            'campaign': serializer.data,
            'attached_data': {}
        }

        # Check the campaign type and retrieve corresponding models
          # Ensure instance.type is treated as a string
        if isinstance(instance.type, str):
            campaign_types = instance.type.strip('{}').split(',')
        elif isinstance(instance.type, list):
            campaign_types = [str(type_item).strip() for type_item in instance.type]
        else:
            campaign_types = []  # Default to an empty list if it's neither
        for campaign_type in campaign_types:
            if campaign_type.strip() == 'email':
                email_campaigns = EmailCampaign.objects.filter(campaign_id=instance.id)
                email_serializer = EmailCampaignSerializer(email_campaigns, many=True)
                response_data['attached_data']['email_campaigns'] = email_serializer.data
            elif campaign_type.strip() == 'instagram':
                instagram_campaigns = InstagramCampaign.objects.filter(campaign_id=instance.id)
                instagram_serializer = InstagramCampaignSerializer(instagram_campaigns, many=True)
                response_data['attached_data']['instagram_campaigns'] = instagram_serializer.data
            elif campaign_type.strip() == 'whatsapp':
                whatsapp_campaigns = WhatsAppCampaign.objects.filter(campaign_id=instance.id)
                whatsapp_serializer = WhatsAppCampaignSerializer(whatsapp_campaigns, many=True)
                response_data['attached_data']['whatsapp_campaigns'] = whatsapp_serializer.data

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class CampaignStatsAPIView(APIView):  # Add this new view
    permission_classes = (AllowAny,)  # Adjust permissions as needed

    def get(self, request):
        total_campaigns = Campaign.objects.count()
        total_revenue = Campaign.objects.aggregate(Sum('expected_revenue'))['expected_revenue__sum'] or 0
        total_actual_cost = Campaign.objects.aggregate(Sum('actual_cost'))['actual_cost__sum'] or 0

        return Response({
            'total_campaigns': total_campaigns,
            'total_revenue': str(total_revenue),  # Convert to string if needed
            'total_actual_cost': str(total_actual_cost),  # Convert to string if needed
        })
    
class InstagramCampaignViewSet(viewsets.ModelViewSet):
    queryset = InstagramCampaign.objects.all()
    serializer_class = InstagramCampaignSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class WhatsAppCampaignViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppCampaign.objects.all()
    serializer_class = WhatsAppCampaignSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

class EmailCampaignViewSet(viewsets.ModelViewSet):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()