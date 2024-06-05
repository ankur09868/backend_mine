from django.shortcuts import render
from rest_framework import generics
from .models import Reminder
from .serializers import ReminderSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

class ReminderListAPIView(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    #permission_classes = (IsAdminUser,)

class ReminderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    # permission_classes = (IsAdminUser,)
