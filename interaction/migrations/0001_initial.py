from django.db import migrations, models
import django.db.models.deletion
from django.contrib.contenttypes.models import ContentType

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(choices=[('Call', 'Call'), ('Email', 'Email'), ('Meeting', 'Meeting'), ('Note', 'Note')], max_length=50)),
                ('interaction_datetime', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('entity_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('entity_id', models.PositiveIntegerField()),
            ],
        ),
    ]
