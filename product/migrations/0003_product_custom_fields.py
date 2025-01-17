# Generated by Django 4.1 on 2024-08-12 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_fields', '0003_alter_customfield_tenant'),
        ('product', '0002_remove_product_vendor_name_product_vendor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='custom_fields',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_custom_fields', to='custom_fields.customfield'),
        ),
    ]
