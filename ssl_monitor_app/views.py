from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServerSSLCertificate, EmailAccounts
from .ssl_service import get_ssl_certificate_details

# Create your views here.
def login(request):
    return render(request, "login.html")


@api_view(["POST"])
def add_server(request):
    requried_fields = ["name", "domain"]
    for field in requried_fields:
        if not request.data.get(field, None):
            return Response(data={"error": "INVALID_ENTRY", "error_message":f"{field} is required"}, status=status.HTTP_417_EXPECTATION_FAILED,exception=True)
        
    new_server_record = ServerSSLCertificate(
        server_name=request.data.get("name"),
        url=request.data.get("domain")
    )
    new_server_record.save()
    get_ssl_certificate_details(request.data.get("domain"))
    return Response({"server": new_server_record.to_dict()},status=status.HTTP_201_CREATED)


@api_view(['POST'])
def force_sync(request):
    if not request.data.get("domain", None):
        return Response(data={"error": "INVALID_ENTRY", "error_message":f"domain is required"}, status=status.HTTP_417_EXPECTATION_FAILED, exception=True)
    updated_servers = get_ssl_certificate_details(request.data.get("domain"))
    return Response({"servers":updated_servers,"count": len(updated_servers)})


@api_view(['GET'])
def get_servers(request):
    """
    List servers available in database.

    Parameters:

    Response:
    - 200 OK: Successful response.
    """
    # user = request.GET.get('user')
    servers = ServerSSLCertificate.objects.all()

    return Response({"servers":[server.to_dict() for server in servers],"count": len(servers)})

@api_view(["POST"])
def update_email_config(request):
    """
    Updates the email configuration based on the request data.

    Parameters:
    - request: The HTTP request object containing the data to update the email configuration.

    Returns:
    - Response: The HTTP response object containing the updated email account in a dictionary format.
    """
    email_account = EmailAccounts.objects.first()
    if email_account:
        email_account.enabled = request.data.get("enabled") or email_account.enabled
        email_account.host = request.data.get("host") or email_account.host
        email_account.port = request.data.get("port")or email_account.port
        email_account.use_tls = request.data.get("use_tls") or email_account.use_tls
        email_account.username = request.data.get("username") or email_account.username
        email_account.password = request.data.get("password") or email_account.password
        email_account.default_sender = request.data.get("default_sender") or email_account.default_sender
        email_account.save()
    else:
        email_account = EmailAccounts(
            host=request.data.get("host"),
            enabled=request.data.get("enabled"),
            port=request.data.get("port"),
            use_tls=request.data.get("use_tls"),
            username=request.data.get("username"),
            password=request.data.get("password"),
            default_sender=request.data.get("default_sender")
        )
        email_account.save()
    return Response({"email_account": email_account.to_dict()})


@api_view(["GET"])
def test_email(request):
    email_account = EmailAccounts.objects.first()
    if email_account:
        res = email_account.test_connection()
        print(res)
    return Response({"email_account": email_account.to_dict()})

@api_view(["GET"])
def get_email_config(request):
    email_account = EmailAccounts.objects.first()
    if email_account:
        return Response({"email_account": email_account.to_dict()})
    else:
        return Response({"email_account": None})