# Generated by Django 4.1 on 2024-08-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_experience_additional_information_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='duration_in_hours',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
