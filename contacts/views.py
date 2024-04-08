from django.shortcuts import render
from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class ContactListCreateAPIView(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = (IsAdminUser,)  # Optionally, add permission classes

class ContactDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = (IsAdminUser,)  # Optionally, add permission classes