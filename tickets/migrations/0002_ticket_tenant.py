# Generated by Django 4.1 on 2024-06-18 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tenant", "0001_initial"),
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="tenant",
            field=models.ForeignKey(
                default="ll",
                on_delete=django.db.models.deletion.CASCADE,
                to="tenant.tenant",
            ),
            preserve_default=False,
        ),
    ]