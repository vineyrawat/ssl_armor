# Generated by Django 5.0.1 on 2024-02-08 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ssl_monitor_app', '0002_emailaccounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaccounts',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
    ]
