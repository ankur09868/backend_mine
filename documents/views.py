from django.shortcuts import render
from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DocumentListAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = (IsAdminUser,)

class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = (IsAdminUser,)


class RetrieveDocumentsView(APIView):
    def get(self, request, entity_type, entity_id=None, *args, **kwargs):
        print(f"Received entity_type: {entity_type}, entity_id: {entity_id}")  
        try:
            content_type = ContentType.objects.get(document=entity_type)
            documents = Document.objects.filter(entity_type=content_type)
            if entity_id:
                documents = documents.filter(entity_id=int(entity_id))
                print(f"Filtered documents: {documents}")  # Debugging line

            documents_data = [{'id': doc.id, 'name':doc.name, 'file': doc.file_url} for doc in documents]

            return Response({'success': True, 'documents': documents_data}, status=status.HTTP_200_OK)
        except ContentType.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid entity_type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

