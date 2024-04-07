from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServerSSLCertificate, EmailAccounts
from .ssl_service import get_ssl_certificate_details
from django.contrib.auth import login
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

# rest_framework imports
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer

# knox imports
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


from ssl_monitor_app.serializers import AuthSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication


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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_servers(request):
    """
    List servers available in database.

    Parameters:

    Response:
    - 200 OK: Successful response.
    """
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
    


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
    
class CreateUserView(generics.CreateAPIView):
    # Create user API view
    serializer_class = UserSerializer