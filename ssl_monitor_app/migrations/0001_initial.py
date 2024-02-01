# Generated by Django 5.0.1 on 2024-02-01 06:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerSSLCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.JSONField(blank=True, null=True)),
                ('issuer', models.JSONField(blank=True, null=True)),
                ('version', models.PositiveIntegerField(blank=True, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=32, null=True)),
                ('not_before', models.DateTimeField(blank=True, null=True)),
                ('not_after', models.DateTimeField(blank=True, null=True)),
                ('subject_alt_name', models.JSONField(blank=True, null=True)),
                ('ocsp', models.URLField(blank=True, null=True)),
                ('ca_issuers', models.URLField(blank=True, null=True)),
                ('crl_distribution_points', models.JSONField(blank=True, null=True)),
                ('server_name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]