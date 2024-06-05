from rest_framework import serializers
from .models import NodeTemplate

class NodeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeTemplate
        fields = "__all__"
