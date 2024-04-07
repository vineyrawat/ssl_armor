import ssl
import socket
from .models import ServerSSLCertificate
from django.utils.timezone import now
from datetime import datetime


def get_ssl_certificate_details(domain):
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443)) as sock:
        try:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                # cert =  json.dumps(cert, indent=2)
                updated_server = update_ssl_details_in_db(domain, cert)
                return updated_server
        except Exception as e:
            print(e)

# certificate_details = get_ssl_certificate_details("core.extensionerp.com")
# print(certificate_details)

def update_ssl_details_in_db(domain, cert):
    servers = ServerSSLCertificate.objects.filter(url=domain)
    for server in servers:
        server.subject = cert.get("subject")
        server.issuer = cert.get("issuer")
        server.version = cert.get("version")
        server.serial_number = cert.get("serialNumber")
        server.not_before = datetime.strptime(cert.get("notBefore"), "%b %d %H:%M:%S %Y %Z")
        server.not_after = datetime.strptime(cert.get("notAfter"), "%b %d %H:%M:%S %Y %Z")
        server.subject_alt_name = cert.get("subjectAltName")
        server.ocsp = cert.get("OSCP")
        server.ca_issuers = cert.get("caIssuers")
        server.modified = now()
        server.save()
    return [server.to_dict() for server in servers]