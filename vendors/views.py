from django.shortcuts import render
from rest_framework import generics
from .models import Vendors
from .serializers import VendorsSerializer
from rest_framework.permissions import IsAdminUser

class VendorsListAPIView(generics.ListCreateAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorsSerializer
    # permission_classes = (IsAdminUser,)

class VendorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorsSerializer
    # permission_classes = (IsAdminUser,)
