# Generated by Django 4.1.5 on 2023-01-15 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_historicalpolicy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='policies', to=settings.AUTH_USER_MODEL),
        ),
    ]
