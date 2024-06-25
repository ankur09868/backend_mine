# Generated by Django 4.1 on 2024-06-20 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0001_initial'),
        ('opportunities', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stage.stage'),
        ),
    ]