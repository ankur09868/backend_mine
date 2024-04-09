from django.shortcuts import render
from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.

from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import Account




from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  # Allowing any user to access this view
    
class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)  # Allowing any user to access this view
