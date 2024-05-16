from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import Interaction

from django.contrib.contenttypes.models import ContentType
from .serializers import InteractionSerializer

class InteractionListAPIView(APIView):
    serializer_class = InteractionSerializer

    def get_queryset(self):
        entity_type = self.request.query_params.get('entity_type')
        entity_id = self.request.query_params.get('entity_id')
        queryset = Interaction.objects.all()

        if entity_type and entity_id:
            try:
                content_type = ContentType.objects.get(model__iexact=entity_type)
                queryset = queryset.filter(entity_type=content_type, entity_id=entity_id)
            except ContentType.DoesNotExist:
                return Interaction.objects.none()  # No results if the content type does not exist

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            entity_type = request.data.get('entity_type')
            entity_id = request.data.get('entity_id')
            interaction_type = request.data.get('interaction_type')
            notes = request.data.get('notes')

            # Get the ContentType object for the specified entity type (case insensitive)
            content_type = ContentType.objects.get(model__iexact=entity_type)

            # Retrieve the entity instance based on entity_id
            entity_instance = content_type.get_object_for_this_type(id=entity_id)

            # Create the Interaction instance
            interaction = Interaction.objects.create(
                entity_type=content_type,
                entity_id=entity_instance.id,
                interaction_type=interaction_type,
                interaction_datetime=datetime.now(),
                notes=notes
            )

            serializer = self.serializer_class(interaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ContentType.DoesNotExist:
            return Response({'error': f"ContentType matching query does not exist for entity type: {entity_type}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred while processing the request: {e}'}, status=status.HTTP_400_BAD_REQUEST)
