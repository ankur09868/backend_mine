from rest_framework import viewsets
from .models import Loyalty
from .serializers import LoyaltySerializer


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class LoyaltyListCreateAPIView(ListCreateAPIView):
    queryset = Loyalty.objects.all()
    serializer_class = LoyaltySerializer

class LoyaltyDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Loyalty.objects.all()
    serializer_class = LoyaltySerializer
