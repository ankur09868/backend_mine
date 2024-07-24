from rest_framework import generics
from .models import drafts
from .serializers import draftsSerializer
from rest_framework.permissions import AllowAny

class DraftListCreateAPIView(generics.ListCreateAPIView):
    queryset = drafts.objects.all()
    serializer_class = draftsSerializer
    permission_classes = (AllowAny,)

class DraftDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = drafts.objects.all()
    serializer_class = draftsSerializer
    permission_classes = (AllowAny,)