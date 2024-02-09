from django.contrib import admin
from .models import ServerSSLCertificate,EmailAccounts,ServerLog

# Register your models here.
admin.site.register(ServerSSLCertificate)
admin.site.register(EmailAccounts)
admin.site.register(ServerLog)