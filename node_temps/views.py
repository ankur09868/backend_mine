from rest_framework import generics
from .models import NodeTemplate
from .serializers import NodeTemplateSerializer
from rest_framework.permissions import IsAuthenticated

class NodeTemplateListCreateAPIView(generics.ListCreateAPIView):
    queryset = NodeTemplate.objects.all()
    serializer_class = NodeTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class NodeTemplateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NodeTemplate.objects.all()
    serializer_class = NodeTemplateSerializer
    permission_classes = [IsAuthenticated]
