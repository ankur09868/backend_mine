from rest_framework import serializers
from .models import Opportunity
from stage.models import Stage  # Assuming Stage model is imported correctly

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('status',)
  
class OpportunitySerializer(serializers.ModelSerializer):
    stage = serializers.PrimaryKeyRelatedField(queryset=Stage.objects.all(), allow_null=True)
    status = serializers.CharField(source='stage.status', read_only=True)

    class Meta:
        model = Opportunity
        fields = (
            'id', 'name', 'amount', 'lead_source', 'probability', 'closedOn',
            'description', 'createdOn', 'isActive', 'account', 
            'contacts', 'closedBy', 'createdBy', 'tenant','stage','status',
        )

