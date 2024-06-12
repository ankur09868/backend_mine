from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import Interaction
from tenant.models import Tenant
from django.contrib.contenttypes.models import ContentType
from .serializers import InteractionSerializer

from django.http import JsonResponse
# from .utils import fetch_entity_details
from interaction.models import Interaction
from django.db.models import Count

from django.views.decorators.http import require_http_methods

import re
import logging
logger = logging.getLogger('simplecrm')
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
            tenant_id = request.data.get('tenant_id')
            notes = request.data.get('notes')

            # Get the ContentType object for the specified entity type (case insensitive)
            content_type = ContentType.objects.get(model__iexact=entity_type)
            tenant = get_object_or_404(Tenant, id=tenant_id)
            # Retrieve the entity instance based on entity_id
            entity_instance = content_type.get_object_for_this_type(id=entity_id)

            # Create the Interaction instance
            interaction = Interaction.objects.create(
                entity_type=content_type,
                entity_id=entity_instance.id,
                interaction_type=interaction_type,
                interaction_datetime=datetime.now(),
                notes=notes,
                tenant=tenant
            )

            serializer = self.serializer_class(interaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ContentType.DoesNotExist:
            return Response({'error': f"ContentType matching query does not exist for entity type: {entity_type}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred while processing the request: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        


def extract_cltv(request, entity_type_id):
    try:
        interactions = Interaction.objects.filter(entity_type_id=entity_type_id)

        report_data = []

        # Iterate over interactions
        for interaction in interactions:
            # Parse notes field to extract amount and contact information
            notes = interaction.notes
            contact = None
            amount = None

            if notes:
                # Use regular expressions to extract contact and amount
                contact_match = re.search(r'Contact: (\w+)', notes)
                amount_match = re.search(r'amount: (\d+)', notes)

                if contact_match:
                    contact = contact_match.group(1)
                if amount_match:
                    amount = amount_match.group(1)

            # Construct report entry
            report_entry = {
                'interaction_type': interaction.interaction_type,
                'interaction_datetime': interaction.interaction_datetime,
                'contact': contact,
                'amount': amount
            }

            # Add report entry to report data list
            report_data.append(report_entry)

            response_data = {'total_interaction':interactions.count(), 'interaction':report_data}

        # Return report data as JSON response
        return JsonResponse(response_data, safe=False)
    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)}, status=500)
class InteractionDetailAPIView(APIView):
    serializer_class = InteractionSerializer

    def get(self, request, pk, *args, **kwargs):
        interaction = get_object_or_404(Interaction, pk=pk)
        serializer = self.serializer_class(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RetrieveInteractionsView(APIView):
    def get(self, request, entity_type, entity_id=None, *args, **kwargs):
        try:
            content_type = ContentType.objects.get(interaction=entity_type)
            if entity_id:
                interactions = Interaction.objects.filter(entity_type=content_type, entity_id=entity_id)
            else:
                interactions = Interaction.objects.filter(entity_type=content_type, entity_id__isnull=True)

            interactions_data = [{'id':inter.id,'interaction_type': inter.interaction_type, 'datetime':inter.interaction_datetime} for inter in interactions]

            return Response({'success': True, 'interactions': interactions_data}, status=status.HTTP_200_OK)
        except ContentType.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid entity_type'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
