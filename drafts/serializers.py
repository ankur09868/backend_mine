from rest_framework import serializers
from .models import drafts

class draftsSerializer(serializers.ModelSerializer):
    class Meta:
        model = drafts
        fields = "__all__"
