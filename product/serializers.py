from rest_framework import serializers
from .models import Product, Experience
from custom_fields.models import CustomField
from custom_fields.serializers import CustomFieldSerializer
from django.contrib.contenttypes.models import ContentType

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"
class ProductSerializer(serializers.ModelSerializer):
    custom_fields = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"

    
    def get_custom_fields(self, obj):
        # Retrieve the ContentType for the Account model
        content_type = ContentType.objects.get_for_model(Product)

        # Filter custom fields for this specific tenant and object_id (Account ID)
        custom_fields = CustomField.objects.filter(
            content_type=content_type,
            object_id=obj.id,
            tenant=obj.tenant
        )

        # Prepare custom fields data
        custom_fields_data = []
        for field in custom_fields:
            custom_fields_data.append({
                'custom_field': field.custom_field,
                'value': field.value,
                'field_type': field.field_type
            })

        return custom_fields_data
    
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"