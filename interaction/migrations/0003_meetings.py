# Generated by Django 4.1 on 2024-08-07 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0002_initial'),
        ('accounts', '0002_initial'),
        ('interaction', '0002_calls'),
    ]

    operations = [
        migrations.CreateModel(
            name='meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Title')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Location')),
                ('from_time', models.DateTimeField(verbose_name='From')),
                ('to_time', models.DateTimeField(verbose_name='To')),
                ('related_to', models.CharField(blank=True, max_length=255, null=True, verbose_name='Related To')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='accounts.account')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting_assigned_users', to=settings.AUTH_USER_MODEL)),
                ('contact_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_contacts', to='contacts.contact', verbose_name='Contact Name')),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_created_by', to=settings.AUTH_USER_MODEL)),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting_hosts', to=settings.AUTH_USER_MODEL, verbose_name='Host')),
                ('participants', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_participants', to='contacts.contact')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
    ]
