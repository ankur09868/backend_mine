# leads/serializers.py

from rest_framework import serializers
from .models import Lead
from custom_fields.models import CustomField
from .models import Stage  # Assuming Stage model is imported correctly

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('status',)


class LeadSerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=Stage.objects.all(), allow_null=True)
    status = serializers.CharField(source='stage.status', read_only=True)

    class Meta:
        model = Lead
        fields = (
            'id', 'title', 'first_name', 'last_name', 'email', 'phone', 'account',
            'source', 'address', 'website', 'description', 'assigned_to',
            'account_name', 'opportunity_amount', 'createdBy', 'createdOn', 'isActive',
            'enquery_type', 'money', 'tenant', 'priority','stage','status'
        )
