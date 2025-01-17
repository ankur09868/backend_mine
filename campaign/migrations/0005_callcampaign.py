# Generated by Django 4.1 on 2024-08-22 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_emailcampaign_email_html'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller_id', models.CharField(max_length=255)),
                ('call_script', models.TextField(blank=True, null=True)),
                ('number_of_calls', models.IntegerField(default=0)),
                ('call_duration', models.DurationField(blank=True, null=True)),
                ('call_outcome', models.CharField(blank=True, max_length=255, null=True)),
                ('successful_calls', models.IntegerField(default=0)),
                ('failed_calls', models.IntegerField(default=0)),
                ('engagement_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='call_campaign', to='campaign.campaign')),
            ],
            options={
                'verbose_name': 'Call Campaign',
                'verbose_name_plural': 'Call Campaigns',
            },
        ),
    ]
