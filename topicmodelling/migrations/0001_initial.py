# Generated by Django 4.1 on 2024-09-05 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0006_remove_contact_flow'),
        ('communication', '0010_sentimentanalysis_contact_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicModelling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topics', models.JSONField()),
                ('contact_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_modelling_contacts', to='contacts.contact')),
                ('conversation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='topic_modelling', to='communication.conversation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_modelling_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
