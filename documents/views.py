from django.shortcuts import render
from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAdminUser


class DocumentListAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = (IsAdminUser,)

class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = (IsAdminUser,)
