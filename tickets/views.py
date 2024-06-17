# tickets/views.py

from rest_framework import generics
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.permissions import IsAdminUser

class TicketListAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # Uncomment the following line to enable admin-only access
    # permission_classes = (IsAdminUser,)

class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # Uncomment the following line to enable admin-only access
    # permission_classes = (IsAdminUser,)
