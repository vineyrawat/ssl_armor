from django.db import models

# Create your models here.
from django.db import models
import django
import uuid
from django.core.mail import EmailMessage, get_connection

class ServerLog(models.Model):
    LOG_LEVEL_CHOICES = [
        ('ERROR', 'Error'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        # Add more choices as needed
    ]

    LOG_TYPE_CHOICES = [
        ('SCHEDULER', 'Scheduler Job'),
        ('EMAIL_QUEUE', 'Email Queue'),
        ('NOTIFICATION', 'Notification'),
        # Add more choices as needed
    ]

    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    title = models.CharField(max_length=100)  # New column for the title
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Additional fields as needed, such as user, IP address, etc.
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.get_level_display()}: {self.title} - {self.message}"

    @classmethod
    def create_scheduler_log(cls, level, title, message):
        return cls.objects.create(level=level, log_type='SCHEDULER', title=title, message=message)

    @classmethod
    def create_email_queue_log(cls, level, title, message):
        return cls.objects.create(level=level, log_type='EMAIL_QUEUE', title=title, message=message)

    @classmethod
    def create_notification_log(cls, level, title, message):
        return cls.objects.create(level=level, log_type='NOTIFICATION', title=title, message=message)



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


from django.db import models

class EmailAccounts(models.Model):
    name =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enabled = models.BooleanField(default=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    use_tls = models.BooleanField(default=True)
    username = models.EmailField()
    password = models.CharField(max_length=100)
    default_sender = models.EmailField()
    creation_time = models.DateTimeField(default=django.utils.timezone.now)
    modified_time = models.DateTimeField(default=django.utils.timezone.now)

    def get_email_backend(self):
        return get_connection(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=self.use_tls,
        )

    def test_connection(self):
        email = EmailMessage(
            subject="Testing Email",
            from_email=self.default_sender,
            to=["vineyrawat@yahoo.com"],
            body="This is a test email.",
            connection=self.get_email_backend()
        )
        try:
            email.send()
            ServerLog.create_email_queue_log("INFO", "Test Email", "Test Email sent successfully")
        except Exception as e:
            ServerLog.create_email_queue_log("ERROR", "Test Email", f"Test Email failed with error: {str(e)}")

    def to_dict(self):
        return {
            'name': self.name,
            'enabled': self.enabled,
            'host': self.host,
            'port': self.port,
            'use_tls': self.use_tls,
            'username': self.username,
            'password': self.password,
            'default_sender': self.default_sender,
            'creation_time': self.creation_time,
            'modified_time': self.modified_time
        }