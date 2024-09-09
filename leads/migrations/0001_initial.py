# Generated by Django 4.1 on 2024-09-06 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '0002_wa'),
        ('accounts', '0002_initial'),
        ('stage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('leads_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('revenue', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total_leads', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True, verbose_name='Treatment Pronouns for the customer')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('source', models.CharField(blank=True, choices=[('call', 'Call'), ('email', 'Email'), ('existing customer', 'Existing Customer'), ('partner', 'Partner'), ('public relations', 'Public Relations'), ('compaign', 'Campaign'), ('other', 'Other')], max_length=255, null=True, verbose_name='Source of Lead')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('website', models.CharField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('description', models.TextField(blank=True, null=True)),
                ('assigned_to', models.CharField(blank=True, max_length=255, null=True)),
                ('account_name', models.CharField(blank=True, max_length=255, null=True)),
                ('opportunity_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Opportunity Amount')),
                ('createdBy', models.CharField(blank=True, max_length=255, null=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('isActive', models.BooleanField(default=False)),
                ('enquery_type', models.CharField(blank=True, max_length=255, null=True)),
                ('money', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Money')),
                ('priority', models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=6, null=True, verbose_name='Lead Priority')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Leads', to='accounts.account')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stage.stage')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
    ]
