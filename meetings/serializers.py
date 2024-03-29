from rest_framework import serializers
from .models import meetings

class meetingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetings
        fields = "__all__"
