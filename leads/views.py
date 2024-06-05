from django.shortcuts import render
from rest_framework import generics
from .models import Lead
from django.http import HttpResponse
from .serializers import LeadSerializer
from rest_framework.permissions import AllowAny  # Import AllowAny
from django.http import JsonResponse
# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class LeadListCreateAPIView(ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (AllowAny,)  # Use AllowAny permission

class LeadDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = (AllowAny,)  # Use AllowAny permission


