from django.db import models

# Create your models here.
from django.db import models
import django

class ServerSSLCertificate(models.Model):
    subject = models.JSONField(blank=True, null=True)
    issuer = models.JSONField(blank=True, null=True)
    version = models.PositiveIntegerField(blank=True, null=True)
    serial_number = models.CharField(max_length=32, blank=True, null=True)
    not_before = models.DateTimeField(blank=True, null=True)
    not_after = models.DateTimeField(blank=True, null=True)
    subject_alt_name = models.JSONField(blank=True, null=True)
    ocsp = models.URLField(blank=True, null=True)
    ca_issuers = models.URLField(blank=True, null=True)
    crl_distribution_points = models.JSONField(blank=True, null=True)
    server_name = models.CharField(max_length=255)
    url = models.URLField()
    creation_time = models.DateTimeField(default=django.utils.timezone.now)
    modified_time = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return f"{self.server_name} - {self.url}"

    def to_dict(self):
        return {
            'subject': self.subject,
            'issuer': self.issuer,
            'version': self.version,
            'serial_number': self.serial_number,
            'not_before': self.not_before,
            'not_after': self.not_after,
            'subject_alt_name': self.subject_alt_name,
            'ocsp': self.ocsp,
            'ca_issuers': self.ca_issuers,
            'crl_distribution_points': self.crl_distribution_points,
            'server_name': self.server_name,
            'url': self.url,
            'creation_time': self.creation_time,
            'modified_time': self.modified_time
        }
