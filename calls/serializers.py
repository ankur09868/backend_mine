from rest_framework import serializers
from .models import calls

class callsSerializer(serializers.ModelSerializer):
    class Meta:
        model = calls
        fields = "__all__"
