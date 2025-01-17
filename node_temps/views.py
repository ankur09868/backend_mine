from rest_framework import generics
from .models import NodeTemplate
from .serializers import NodeTemplateSerializer
from rest_framework.permissions import IsAuthenticated

class NodeTemplateListCreateAPIView(generics.ListCreateAPIView):
    queryset = NodeTemplate.objects.all()
    serializer_class = NodeTemplateSerializer
    

   

class NodeTemplateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NodeTemplate.objects.all()
    serializer_class = NodeTemplateSerializer
  
